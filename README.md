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


-----------------------------------------------------------
`pair_style  gran model hertz tangential history cohesion sjkr rolling_friction cdt `

--> 

`pair_style  gran model hertz tangential history cohesion sjkr rolling_friction cdt surface superquadric`

-----------------------------------------------------------
`fix granwalls all wall/gran model hertz tangential history cohesion sjkr rolling_friction cdt  mesh n_meshes 1 meshes cad`

-->

`fix granwalls all wall/gran model hertz tangential history cohesion sjkr rolling_friction cdt surface superquadric mesh n_meshes 1 meshes cad `

-----------------------------------------------------------
`fix pts1 all particletemplate/sphere 15485863 atom_type 1 density constant ${DENSITY} radius constant ${RADIUS}`

-->

`fix pts1 all particletemplate/superquadric 15485863 atom_type 1 density constant 2500 shape constant ${RADIUS} ${RADIUS} ${RADIUS} blockiness constant 1.0 1.0`

This makes a sphere with the radius RADIUS, change the Blockiness constants to get other shapes

-----------------------------------------------------------
`fix     integr all nve/sphere`

-->

`fix		integr all nve/superquadric`

-----------------------------------------------------------

for dumping use:

`dump dmp2 all custom/vtk 2000 post/dump*.superq.vtk type mass x y z id vx vy vz fx fy fz omegax omegay omegaz radius shapex shapey shapez quat1 quat2 quat3 quat4 blockiness1 blockiness2 tqx tqy tqz angmomx angmomy angmomz`


## Paraview Setup (Version 5.8)

1. Load dump*.superq.vtk
2. Add Sources --> Superquadric
    - Center 0,0,0
    - Theta Roundness is 2/blockiness1
    - Phi Roundness is 2/blockiness2
    - untoggle Toroidal
    ( blockiness1/2 correspond to the first and second value for blockiness in the particletemplate/superquadric command )
3. Add a transform filter to Superquardic
    - rotate  in x axis by 90 (°)
    - scale your particle to your particle size
4. ctrl+ click on dump*.superq.vtk and Superquadric (first sump, than quadric)
    - apply programmamble filter
    - Output : vtkUnstructuredGrid
    - Code: copy from  __transform_filter_superquadric_with_colors.py__
5. Apply and enjoy



## Credits
User: 
martin.kozakovic 
and
richti83

on website www.cfdem.com



## Sources:
https://www.cfdem.com/forums/tutorial-4-superquadric-angle-repose-representation-python-filter


