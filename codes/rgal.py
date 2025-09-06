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
        gal_com_x, gal_com_y, gal_com_z, total_m = 0, 0, 0, 0

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

            gal_com_x += float(line[8]) * float(line[13]) * 6e10 * float(line[0])
            gal_com_y += float(line[8]) * float(line[13]) * 6e10 * float(line[1])
            gal_com_z += float(line[8]) * float(line[13]) * 6e10 * float(line[2])
            total_m += float(line[8])*float(line[13])*6e10


        gal_com_x /= total_m
        gal_com_y/= total_m
        gal_com_z /= total_m
        
        ngas = len(iwas_list)
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

                if len(gmc_par) < 2:
                    continue

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

        ang_dict = {}
        for gmc, values in gmc_com.items():
            L = [0.0 ,0.0 ,0.0 ]
            loc_m = 0.0
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

                loc_m += m_par

            gal_dist = math.sqrt((com_list[0]-gal_com_x)**2 + (com_list[1]-gal_com_y)**2 + (com_list[2]-gal_com_z)**2)

            L_mag = math.sqrt(L[0]**2 + L[1]**2 + L[2]**2)/loc_m
            ang_dict[gal_dist] = L_mag

        print(ang_dict)

        break
