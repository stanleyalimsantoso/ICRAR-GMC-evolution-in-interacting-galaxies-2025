import math
with open("tout.dat", "r") as file:
    current_snap = 0
    desired_snap = 4
    gmc_mass_list = []
    while True:
        header = file.readline().split()
        if not header:
            break

        num_bodies = int(header[0])

        file.readline()
        file.readline()
        file.readline()

        iwas_list, position, mj, frah = [], [], [], []

        if current_snap < desired_snap:
            for i in range(num_bodies):
                file.readline()
            current_snap += 1
            continue

        for i in range(num_bodies):
            line = file.readline().split()
            if len(line) < 14:
                continue

            iwas = int(float(line[6]))

            if iwas == 2:
                iwas_list.append(iwas)
                position.append([float(x) for x in line[0:3]])
                mj.append(float(line[8]))
                frah.append(float(line[13]))

        ngas = len(iwas_list)
        visited = [False] * ngas

        for i in range(ngas):
            if visited[i] == False:
                visited[i] = True
                m = mj[i]*frah[i]
                if m == 0:
                    continue

                for j in range(ngas):
                    if i == j:
                        continue
                    if visited[j] == True:
                        continue

                    dx = position[i][0] - position[j][0]
                    dy = position[i][1] - position[j][1]
                    dz = position[i][2] - position[j][2]

                    r = (dx*dx + dy*dy + dz*dz) ** 0.5
                    if r <= 0.1:
                        visited[j] = True
                        m += mj[j]*frah[j]

                gmc_mass_list.append(m * 6*10**10)

        print(f"DEBUG: found {len(gmc_mass_list)} GMCs")
        break

    bin_centers = [10**(4 + 0.3*(i+0.5)) for i in range(10)]

    bin_counts = {c: 0 for c in bin_centers}
    bin_width  = 0.3


    for m in gmc_mass_list:
        if m <= 0:
            continue
        logm = math.log10(m)
        if 4 <= logm < 7:
            k = int((logm - 4) / bin_width)
            bin_counts[bin_centers[k]] += 1

    print(bin_counts)

    total_mass = sum(gmc_mass_list)
    mean_mass = total_mass/len(gmc_mass_list)

    checker = 0
    for i in gmc_mass_list:
        if i >= 10**6:
            checker +=1

    fraction = checker/len(gmc_mass_list)

    print("mean mass: ", mean_mass)
    print("Large GMC fraction: ", fraction)
