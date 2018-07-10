***!! WARNING: Save and backup any files you hope to change, I am not responsible for broken games !!***


* Whats needed:
    * <path_to_mod>

    * /map
        * /default.map
        * /positions.txt
        * /heightmap.bmp
        * /provinces.bmp
        * /rivers.bmp
        * /terrain.bmp
        * /trees.bmp
        * /world_normal.bmp
    
    * /map/random/*.bmp
    
    * /map/terrain
        * /colormap_autumm.dds
        * /colormap_spring.dds
        * /colormap_summer.dds
        * /colormap_winter.dds
        * /colormap_water.dds

    * /common/tradenodes/00_tradnodes.txt

1) Run the script:
    ./flip.py <path_to_file>
    
    where <path_to_file> points to the folder containing the mod

2) Manually flip each file enfing in .bmp, or .dds extensions
    * can be done in ms paint for .bmp
    * or gimp2 for .dds
    * probably a way easier way to do this, but I couldn't be bothered

3) You may need to flip any files relating to canals, they will be in the /map folder and in /map/default.map   