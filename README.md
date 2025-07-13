# ICRAR-GMC-evolution-in-interacting-galaxies-2025
This repository contains results and selected sample codes I developed to investigate the evolution of giant molecular clouds (GMCs) in simulations of interacting and merging galaxies.

This is part of a research project I've been working on since April 2025, supervised by A/Prof Kenji Bekki at the International Centre for Radio Astronomy Research (ICRAR). The full title is: "Formation and evolution of massive stars and giant molecular clouds (GMCs) in interacting and merging galaxies."

## What I'm doing
The simulations were written by Kenji and run using the OzSTAR supercomputer. My job is to run different setups of the simulation(e.g. isolated vs interacting galaxies) and analyse how tidal forces and collisions affect the formation of GMCs. To explain more, GMCs form when HI (atomic hydrogen) gas clumps together in a localised region and becomes dense enough to convert to H₂ (molecular hydrogen). GMCs are the birthplaces of stars, as clouds of H₂ gas contract and heat up, forming protostars that will eventually begin hydrogen fusion in their cores. When galaxies interact or collide, they generate tidal forces, which stretch and distort the structure of the galaxies, potentially helping or hindering the formation of GMCs.

First, let's do an isolated galaxy run and see how H₂ gas and new stars evolve normally. Running Kenji's simulation gives 6 snapshots of how the galaxy looks at different intervals over 1.4 Gyr(that's 1.4 billion years!)

### H2 and Star Formation in Isolated Galaxies
<p float="left">
  <img src="images/Isolated H2 mass time evolution picture.png" width="45%" />
  <img src="images/isolated new star time evolution picture.png" width="45%" />
</p>

Here, we can see how H₂ gases (left) and new stars (right) form and evolve over time. Initially, the H2 gas is evenly spread out across the galaxy, with no stars present. After some time, the H₂ gas clumps together to form GMCs, which then trigger star formation. Visually, we can see an increasing number of stars as the simulation progresses.

To analyse the data, I developed the code *parsetout.py*, which does a simple job of calculating each of the particles' mass and summing them up according to their types (e.g. gas, new star, old star), for each timestep. But before showing the results, let's see how the distribution of stars and gases changes over time in an interacting galaxy. In the interacting model, we simulated a galaxy passing by with a single particle weighing 0.1, 0.3, and 1.0 times that of the original galaxy's mass.

### H2 and Star Formation in 0.1 Mass Interacting Galaxy
<p float="left">
  <img src="images/interacting 0.1 ratio H2 mass time evolution picture.png" width="45%" />
  <img src="images/interacting 0.1 ratio new stars time evolution picture.png" width="45%" />
</p>

Again, the H₂ gases (left) and new stars (right). We see that at the third timestep, a pass-by has occurred, and the structure of the galaxy changes drastically before eventually settling in again. The turbulence causes star formation to be more active in certain regions in the outer layers, indicated by the bright clumps of new stars in the picture.

### H2 and Star Formation in 0.3 Mass Interacting Galaxy
<p float="left">
  <img src="images/interacting 0.3 ratio H2 mass time evolution picture.png" width="45%" />
  <img src="images/interacting 0.3 ratio new stars time evolution picture.png" width="45%" />
</p>

Now we see that a much more violent interaction has occurred. The structure of the galaxy is completely broken, leaving only scattered GMCs. Now, surely such a violent interaction impacts the formation and evolution of GMCs. We only need to see one more case after this and we will continue
