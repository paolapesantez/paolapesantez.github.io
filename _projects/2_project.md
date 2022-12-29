---
layout: page
title: Software Development to Simulate Irradiation of Skin
description: Kinetic Model of Development and Aging of Artificial Skin Based on Analysis of Microscopy Data
img: assets/img/layers21days.webp
importance: 2
category: work
---

For the development of this project, computational tools were created in Fortran, Bash, and MATLAB to gather, process, and fit experimental data resulting from the Monte-Carlo simulation of low energy electron particle tracks in liquid water using the Positive Ion Track Simulation (PITS) code set.

To gather the data, the experimental space was packed with 1 micron diameter spheres in concentric rings to exploit angular symmetry.One million tracks were generated for initial beam energies of 25keV, 50keV, 80keV, and 90keV, on an 8 node PC cluster.  Then, computational routines covering a given B-spline library were created to approximate the probability distributions and summary statistics for any stochastic quantity over a domain of target location and beam energy. Finally, some studies were undertaken such as: determining whether the representations developed for the one micron diameter spheres could be applied to larger targets by packing the targets with the spheres and somehow aggregating the results, developing our own Kinetic Monte Carlo Simulation in order to obtain cell counts at multiple continuous times and thus predict thickness of layers of the skin, and relating the results from PITS with another investigation about height of layers (thickness), cell counts at particular times in such a way that we can update PITS' parameters and calculate the amount of energy deposited at the different layers of skin at different thicknesses.  
MSc Thesis - Advisor: John Miller, PhD.

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.html path="assets/img/skinlayers.png" title="" class="img-fluid rounded z-depth-1" %}
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.html path="assets/img/confocalperspective.webp" title="" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.html path="assets/img/spheres.webp" title="" class="img-fluid rounded z-depth-1" %}
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.html path="assets/img/contour_plot.webp" title="" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="row"> 
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.html path="assets/img/bsplineat25kev.webp" title="" class="img-fluid rounded z-depth-1" %}
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.html path="assets/img/layers21days.webp" title="" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
   Aging of Artificial Skin Based on Analysis of Microscopy Data
</div>