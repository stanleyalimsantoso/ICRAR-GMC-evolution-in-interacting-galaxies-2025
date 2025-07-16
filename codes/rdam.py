import math
def cross(a, b):
    c = [a[1]*b[2] - a[2]*b[1],
         a[2]*b[0] - a[0]*b[2],
         a[0]*b[1] - a[1]*b[0]]

    return c

current_snap = 0
desired_snap = 4

with open("tout.dat", "r") as file:
    while True:
        header = file.readline().split()
        if not header:
            break

        num_bodies = int(header[0])

        file.readline()
        file.readline()
        file.readline()

        if current_snap < desired_snap:
            for i in range(num_bodies):
                file.readline()
            current_snap += 1
            continue

        iwas_list, position, velocities, mj, frah = [], [], [], [], []
        
        for i in range(num_bodies):
            line = file.readline().split()
            if len(line) < 14:
                continue

            iwas = int(float(line[6]))

            if iwas == 2:
                iwas_list.append(iwas)
                position.append([float(x) for x in line[0:3]])
                velocities.append([float(x) for x in line[3:6]])
                mj.append(float(line[8]))
                frah.append(float(line[13]))

        ngas = len(iwas_list)

        print(f"DEBUG: snapshot={current_snap}, gas particles (iwas==2) = {len(iwas_list)}")

        visited = [False] * ngas

        gmc_com = {}

        print("calculating centre of mass of each GMC")

        count = 0
        for i in range(ngas):
            if visited[i] == False:
                visited[i] = True
                m = mj[i]*frah[i]*6e10
                if m == 0:
                    continue
                count += 1

                loc_com_x, loc_com_y, loc_com_z = [mj[i] * frah[i] * 6e10 * position[i][k] for k in range(3)]
                loc_com_vx, loc_com_vy, loc_com_vz = [mj[i] * frah[i] * 6e10 * velocities[i][k] for k in range(3)]
                gmc_par = {}
                gmc_par[0] = [position[i][0], position[i][1], position[i][2], velocities[i][0], velocities[i][1], velocities[i][2], m]

                j_count = 0
                for j in range(ngas):
                    if i == j:
                        continue
                    if visited[j] == True:
                        continue

                    dx = position[i][0] - position[j][0]
                    dy = position[i][1] - position[j][1]
                    dz = position[i][2] - position[j][2]

                    r = math.sqrt(dx*dx + dy*dy + dz*dz)
                    if r <= 0.1:
                        visited[j] = True
                        m += mj[j]*frah[j]*6e10
                        j_count += 1


                        loc_com_x += mj[j] * frah[j] * position[j][0] * 6e10
                        loc_com_y += mj[j] * frah[j] * position[j][1] * 6e10
                        loc_com_z += mj[j] * frah[j] * position[j][2] * 6e10
                        loc_com_vx += mj[j] * frah[j] * velocities[j][0] * 6e10
                        loc_com_vy += mj[j] * frah[j] * velocities[j][1] * 6e10
                        loc_com_vz += mj[j] * frah[j] * velocities[j][2] * 6e10

                        gmc_par[j_count] = [position[j][0], position[j][1], position[j][2], velocities[j][0], velocities[j][1], velocities[j][2], mj[j] * frah[j] * 6e10]

                com_list = [loc_com_x/m, loc_com_y/m, loc_com_z/m, loc_com_vx/m, loc_com_vy/m, loc_com_vz/m]
                max_x, max_y, max_z, max_r = 0, 0, 0, 0

                for index, par_info in gmc_par.items():
                    x_par, y_par, z_par = [com_list[i] - par_info[i] for i in range(3)]

                    par_r = math.sqrt(x_par**2 + y_par**2 + z_par**2)
                    if par_r >= max_r:
                        max_x = x_par
                        max_y = y_par
                        max_z = z_par
                        max_r = par_r


                gmc_com[count] = [m, com_list, max_r, gmc_par]

        choice = int(input(f"There are {len(gmc_com)} GMCs available, which one do you want to analyse?"))

        radial_density = []
        dist_list = []

        rad = gmc_com[choice][2]
        yplot = [i for i in range(1, 101)]
        com_list = gmc_com[choice][1]

        print("building radial density profile")
        for i in range(0, 30):
            check_rad_in = rad * i / 30
            check_rad_out = rad * (i+1)/30
            check_m = 0
            check_vol = math.pi * 4 / 3 * (check_rad_out**3 - check_rad_in**3)
            for par in gmc_com[choice][3].values():
                dx = par[0] - com_list[0]
                dy = par[1] - com_list[1]
                dz = par[2] - com_list[2]

                par_rad = math.sqrt(dx*dx + dy*dy + dz*dz)

                if check_rad_in < par_rad <= check_rad_out:
                    check_m += par[6]
            radial_density.append(check_m/check_vol)
            dist_list.append((check_rad_in + check_rad_out)*0.5)

        final_rad_density = {dist_list[i]: radial_density[i] for i in range(len(radial_density))}
        print(final_rad_density)

        print("calculating angular momentum")
        L = [0.0 ,0.0 ,0.0 ]
        total_m = 0.0
        for par in gmc_com[choice][3].values():
            dx = (par[0] - com_list[0])
            dy = (par[1] - com_list[1])
            dz = (par[2] - com_list[2])

            dvx = (par[3] - com_list[3])
            dvy = (par[4] - com_list[4])
            dvz = (par[5] - com_list[5])

            m_par = par[6]

            r = [dx, dy, dz]
            v = [dvx, dvy, dvz]

            a,b,c = cross(r, v)
            L[0] += a*m_par
            L[1] += b*m_par
            L[2] += c*m_par

            total_m += m_par

        L_mag = math.sqrt(L[0]**2 + L[1]**2 + L[2]**2)

        print(L_mag/total_m)

      #angular momentum distribution -> only need once
        ang_dict = {}
        for gmc, values in gmc_com.items():
            L = [0.0 ,0.0 ,0.0 ]
            total_m = 0.0
            com_list = values[1]
            for par in values[3].values():
                dx = (par[0] - com_list[0])
                dy = (par[1] - com_list[1])
                dz = (par[2] - com_list[2])

                dvx = (par[3] - com_list[3])
                dvy = (par[4] - com_list[4])
                dvz = (par[5] - com_list[5])

                m_par = par[6]

                r = [dx, dy, dz]
                v = [dvx, dvy, dvz]

                a,b,c = cross(r, v)
                L[0] += a*m_par
                L[1] += b*m_par
                L[2] += c*m_par

                total_m += m_par

            L_mag = math.sqrt(L[0]**2 + L[1]**2 + L[2]**2)/total_m
            ang_dict[total_m] = L_mag

        print(ang_dict)

        break
