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

`fix pts1 all particletemplate/superquadric 15485863 atom_type 1 density constant 2500 shape constant ${RADIUS1} ${RADIUS2} ${RADIUS3} blockiness constant ${BLOCK1} ${BLOCK2}`

 Play arround in parraview (next chapter) to find your desired shape

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
    - Theta Roundness is 2/${BLOCK1}
    - Phi Roundness is 2/${BLOCK2}
    - untoggle Toroidal
3. Add a transform filter to Superquardic
    - rotate  in x axis by 90 (°)
    - scale your particle to your particle size
        - x scale is ${RADIUS1}*2
        - y scale is ${RADIUS3}*2
        - z scale is ${RADIUS2}*2
    - if you want to see the overall dimensions of your particle go to the "information" tab. (Bounds, delta for each dimension is the size in m (usually ))
4. ctrl+ click on dump*.superq.vtk and Superquadric (first dump, than superquadric)
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


