h2mass_time = {}
with open("tout.dat", "r") as file:
        while True:
                header = file.readline().split()
                if not header:
                        break

                num_bodies = int(header[0])
                time = float(header[1])
                total_h2mass = 0.0

                file.readline()
                file.readline()
                file.readline()

                for i in range(num_bodies):
                        line = file.readline().split()
                        if len(line) < 14:
                                continue
                        try:
                                iwas = int(line[6])
                        except (ValueError, IndexError):
                                continue
                        if iwas == 3: #2 is for gas, 3 is for new stars
                                mj = float(line[8])
                                frah = float(line[13])
                                h2mass = mj * frah

                                total_h2mass += h2mass

                h2mass_time[time] = total_h2mass
print(h2mass_time)
