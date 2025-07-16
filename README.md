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

To analyse the data, I developed the code *parsetout.py*, which does a simple job of calculating each of the particles' mass(in solar mass units) and summing them up according to their types (e.g. gas, new star, old star), for each timestep. But before showing the results, let's see how the distribution of stars and gases changes over time in an interacting galaxy. In the interacting model, we simulated a galaxy passing by with a single particle weighing 0.1, 0.3, and 1.0 times that of the original galaxy's mass.

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

In this case, the interaction is noticeably more violent. The structure of the galaxy is completely disrupted, leaving only scattered GMCs. Such a strong interaction clearly has a major impact on the formation and evolution of GMCs. One more case remains to be examined

### H2 and Star Formation in 1.0 Mass Interacting Galaxy
<p float="left">
  <img src="images/interacting 1.0 ratio H2 mass time evolution picture.png" width="45%" />
  <img src="images/interacting 1.0 ratio new stars time evolution picture.png" width="45%" />
</p>

The final case is a very extreme interaction, a 1-1 mass ratio encounter. The interaction completely destroys the original galactic structure, which leaves GMCs scattered and dispersed. The system is too chaotic and turbulent that we are left with nothing in the last frame.

### H2 and Star Formation Plots
<p float="left">
  <img src="images/combined H2 graph(3).png" width="45%" />
  <img src="images/combined new star graph.png" width="45%" />
</p>

H₂ formation increases with the strength of interaction. The stronger the interaction, the more H₂ gas is produced. However, if the interaction is too strong, like in the 1.0 mass ratio case, the system becomes too chaotic for the H₂ gas to settle and form GMCs. This explains why the 1.0 case has roughly the same number of new stars as the isolated case. The 0.3 mass ratio seems to benefit GMC formation the most, producing 3x more stars than the isolated case

### Weaker vs Stronger Interaction 

We can vary the strength of the interaction without changing the mass ratio of the galaxy by adjusting two orbital parameters:
- Pericentre distance
  The shortest distance between the main and the companion galaxy. A smaller pericentre distance produces a stronger tidal force
- Orbit eccentricity
  Describes the shape of the orbit.
  - e = 0 is a circular orbit
  - 0 < e < 1 is an elliptical orbit
  - e = 1 is a parabolic orbit.

We now examine a 0.3-mass-ratio companion. In the previous run, the pericentre distance was 1 code unit and the eccentricity was 0.8. Here we increase the pericentre to 2.0 code units and set e = 1.0.

<p float="left">
  <img src="images/weaker interaction H2 gas time evolution picture.png" width="45%" />
  <img src="images/weaker interaction new star time evolution picture.png" width="45%" />
</p>


A larger pericentre and higher eccentricity create a weaker interaction, allowing the galaxy structure to remain intact after the interaction.

<p float="left">
  <img src="images/stronger vs weaker interaction H2 gas.png" width="45%" />
  <img src="images/stronger vs weaker interaction new stars.png" width="45%" />
</p>

The weaker interaction leads to less H₂ and slow new star formation. The stronger interaction burns through the H₂ much quicker, triggering an early burst of new stars.

Now that we have seen how tidal forces impact the formation of GMCs, consider the spread of the masses of the GMCs. The GMC mass function describes the mass distribution of the GMCs. Using the code *gmc_mass.py*, we can get a clear look at the mass function.

*gmc_mass.py* detects GMCs by visiting an unvisited particle and then flagging all nearby particles as a cloud. It then bins through the mass of each cloud and returns the mean mass and the percentage of clouds with a mass greater than 10^6.

<p float="left">
  <img src="images/GMC MASS FUNCTION NEW T = 4 COMBINED.png" width="80%" />
</p>

- mean mass
   - Interacting: 6331654.416293271 solar mass
   - Isolated: 9547133.997058632 solar mass
- fraction of high-mass GMC(>10^6)
   - Interacting: 0.4230769230769231
   - Isolated: 0.7228260869565217

At T = 8(fourth timestep, corresponding to 1.13 Gyr), there is a clear difference in the mass function. In the isolated case, there are fewer low-mass GMCs and many high-mass GMCs, while the distribution in the interacting case is more even. This result is not in agreement with observation, which shows that interacting galaxies usually have more high-mass GMCs. The discrepancy here might be caused by limited resolution(not enough particles) or issues in the detection algorithm.


  
