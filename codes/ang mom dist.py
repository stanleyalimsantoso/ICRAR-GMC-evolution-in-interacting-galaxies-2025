import collections

MASS_SCALE = 6e10
current_snap = 0
desired_snap = 4
R_THRESH = 0.1
R_THRESH2 = R_THRESH * R_THRESH

with open("tout.dat", "r") as file:
    while True:
        header = file.readline().split()
        if not header:
            break
        num_bodies = int(header[0])
        file.readline(); file.readline(); file.readline()
        if current_snap < desired_snap:
            for _ in range(num_bodies):
                file.readline()
            current_snap += 1
            continue

        x = []; y = []; z = []
        vx = []; vy = []; vz = []
        mj = []; frah = []
        ref_found = False
        xref = yref = zref = vxref = vyref = vzref = 0.0

        for _ in range(num_bodies):
            line = file.readline()
            if not line:
                break
            cols = line.split()
            if len(cols) < 14:
                continue
            iw = int(float(cols[6]))
            xi = float(cols[0]); yi = float(cols[1]); zi = float(cols[2])
            vxi = float(cols[3]); vyi = float(cols[4]); vzi = float(cols[5])
            if (not ref_found) and iw == 1:
                ref_found = True
                xref = xi; yref = yi; zref = zi
                vxref = vxi; vyref = vyi; vzref = vzi
            if iw == 2:
                x.append(xi); y.append(yi); z.append(zi)
                vx.append(vxi); vy.append(vyi); vz.append(vzi)
                mj.append(float(cols[8]))
                frah.append(float(cols[13]))

        if not ref_found:
            print("classifying GMC spin (up/down); ngas =", 0)
            print([])
            print("\n" * 5)
            print([])
            break

        n = len(x)
        for i in range(n):
            x[i]  -= xref
            y[i]  -= yref
            z[i]  -= zref
            vx[i] -= vxref
            vy[i] -= vyref
            vz[i] -= vzref

        for i in range(len(x)-1, -1, -1):
            xr = x[i]; yr = y[i]; zr = z[i]
            if xr*xr + yr*yr + zr*zr > 1.0:
                del x[i]; del y[i]; del z[i]
                del vx[i]; del vy[i]; del vz[i]
                del mj[i]; del frah[i]

        ngas = len(x)
        print("classifying GMC spin (up/down); ngas =", ngas)

        if ngas == 0:
            print([])
            print("\n" * 5)
            print([])
            break

        visited = [0]*ngas
        poszlist, negzlist = [], []
        MASS = MASS_SCALE
        thr2 = R_THRESH2

        for i in range(ngas):
            if visited[i]:
                continue
            q = collections.deque([i])
            visited[i] = 1
            members = [i]
            while q:
                a = q.popleft()
                xa = x[a]; ya = y[a]; za = z[a]
                for j in range(ngas):
                    if visited[j]:
                        continue
                    dx = xa - x[j]; dy = ya - y[j]; dz = za - z[j]
                    if dx*dx + dy*dy + dz*dz <= thr2:
                        visited[j] = 1
                        members.append(j)
                        q.append(j)
            if len(members) < 2:
                continue
            m_tot = 0.0
            x_tot = y_tot = z_tot = 0.0
            vx_tot = vy_tot = vz_tot = 0.0
            for j in members:
                m = mj[j] * frah[j] * MASS
                m_tot += m
                x_tot += m * x[j]; y_tot += m * y[j]; z_tot += m * z[j]
                vx_tot += m * vx[j]; vy_tot += m * vy[j]; vz_tot += m * vz[j]
            if m_tot == 0.0:
                continue
            x_com = x_tot / m_tot
            y_com = y_tot / m_tot
            vx_com = vx_tot / m_tot
            vy_com = vy_tot / m_tot
            Lz = 0.0
            for j in members:
                m = mj[j] * frah[j] * MASS
                rx = x[j] - x_com
                ry = y[j] - y_com
                vxr = vx[j] - vx_com
                vyr = vy[j] - vy_com
                Lz += m * (rx * vyr - ry * vxr)
            if Lz >= 0.0:
                poszlist.append([x_com, y_com])
            else:
                negzlist.append([x_com, y_com])

        print(poszlist)
        print("\n" * 5)
        print(negzlist)
        break
