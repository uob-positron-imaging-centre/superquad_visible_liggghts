# How To Simulate superquadric particles in liggghts and make them visible in paraview 5.8

Liggghts must be compiled with 
USE_SUPERQUADRICS = "ON"
in makefile.user in the src/MAKE/ folder

## Liggghts simulation setup:
use your normal simulation file. Change following lines:
( your settings may be different, change accordingly)

`atom_style      granular `
--> 
`atom_style 	    superquadric`

`pair_style  gran model hertz tangential history cohesion sjkr rolling_friction cdt `
--> 
`pair_style  gran model hertz tangential history cohesion sjkr rolling_friction cdt surface superquadric`

`fix granwalls all wall/gran model hertz tangential history cohesion sjkr rolling_friction cdt  mesh n_meshes 1 meshes cad`
-->
`fix granwalls all wall/gran model hertz tangential history cohesion sjkr rolling_friction cdt surface superquadric mesh n_meshes 1 meshes cad `

`fix pts1 all particletemplate/sphere 15485863 atom_type 1 density constant ${DENSITY} radius constant ${RADIUS}`
-->
`fix pts1 all particletemplate/superquadric 15485863 atom_type 1 density constant 2500 shape constant ${RADIUS} ${RADIUS} ${RADIUS} blockiness constant 1.0 1.0`
This makes a sphere with the radius RADIUS, change the Blockiness constants to get other shapes
 
`fix     integr all nve/sphere`

-->

`fix		integr all nve/superquadric`


