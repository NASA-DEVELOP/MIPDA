# MIPDA
MIPDA (Mapping Insect and Pathogen Disturbance Automation)

Project: Glacier National Park Climate II
Locations: LaRC Spring 2017


For studying the climate of Glacier National Park, project members did ArcMap
processing with a Landsat time series that was automated in Python.
This software contains many different parts and each has a different capability. Part 1
involves clipping Landsat scenes to a predetermined study area. Part 2 gives pixels that
contain clouds a value of No Data. Part 3 combines these cloud-free Landsat scenes
into one mosaicked image for each year based on a target date. Part 4 calculates
interannual DNDMI for each specified interannual period. Part 5 subsets Aerial
Detection Survey (ADS) polygons to bark beetle and dead trees per acre. Parts 6, 7,
and 8 subset DNDMI to ADS polygons, healthy vegetation polygons, and fire polygons
respectively, and part 9 generates histograms for parts 6, 7, and 8. Finally part 10
produces classification maps and part 11 creates frequency maps.

Validation for the code occurred throughout the individual creation and completion of the
following components:
1. Clipping Landsat raw Landsat scenes
2. Cloud masking Landsat scenes
3. Mosaicing Landsat scenes
4. Attaining ∆NDMI rasters
5. Subsetting ADS polygons to bark beetle and DTPA
6. Subsetting ∆NDMI to bark beetle DTPA, healthy forest, and fire polygons
7. Create histograms from subsets and obtain thresholds for disturbance categories
8. Creating classification maps from reclassified thresholds
9. Creating frequency maps for moderate disturbance from classification maps

Technical Point of Contact
Antonio Alvarado
antonioalvaradojr@gmail.com
