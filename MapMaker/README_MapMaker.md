<h1>ReadMe for Mapmaker V0.1</h1>

<h3>How to Use</h3>
<p>The mapmaker is a tool meant to help with an overall design of a world's map. It includes various biomes, each of which can be assigned various traits and interesting features. The assignment of biome, trait and features is entirely random, but will populate the map with cities, towns, dungeons, and other features a D&D adventuring party might be interested in.</p>

<h3>Color Legend</h3>
<p>Light Green - Grassland Biome (This includes savannahs)</p>
<p>Dark Green - Forest Biome (This includes marshes and swamps)</p>
<p>Blue - Aquatic Biome (This includes lakes and seas)</p>
<p>Light Yellow - Desert</p>
<p>Medium Yellow - Beach (This biome includes dried up seas and canyons formed by water)</p>
<p>White - Tundra</p>

<h3>Functions & Classes</h3>

<h4>HexBox Class</h4>
<p>init: Creates the hexbox, the hexbox includes several fields.
- x: This is the initial x location I want to build the hex around
- y: This is the initial y location I want to build the hex around
- xPoint: This is a tracker of all the points that make up the hex
- yPoint: This is a tracker of all the points that make up the hex
- traits: This is a list of the traits in the hex.
- traitDescription: This is a growing paragraph of the descriptions of the traits
- number: this is number of the hex, currently unused.
- biome: This is a string of the biome of the hex.
- active: This is a bool of whether the hex is active, currently unused
- color: This is the color I want for the hex, initialized to green
- radius: this is the radius (the length of each line)
- location: this is the column/row location of the hex.
</p>
<p>traitAssign: This assigns the biome for the hex, as well as assigns the traits and trait descriptions to the hex, it is called before the draw function.
- biomeNum: A random number which decides what biome the hex will be
- firstTrait: a random number, picking the first trait
- secondTrait: a random number, picking the second trait
- thirdTrait: a random number, picking the third trait
- fourthTrait: a random number, picking the fourth trait
- fifthTrait: a random number, picking the fifth trait
- sixthTrait: a random number, picking the sixth trait

</br> The traits are picked randomly and get a single check for whether they match or not. While this doesn't prevent the traits from matching up, it does ensure that most won't match up. When I tried to use a while loop on this, it broke.

</br> The traits, when sorted, have the last character removed (the \n) and are then searched for in the document to gather their descriptions.</p>
<p>draw: Draw creates the hexes on the screen. It first creates the colored hex, and then creates the black outline for it.</p>

<h4>mapDraw Function</h4>
<p>mapDraw is the function which draws the initial map, calls the HexBox functions, and controls it's creation. This is called before the while loop in the game so it's only called once unless the restart button is hit. It draws the hexes based on the gridding system, and assigns them their column and row.</p>

<h4>cleanScreen Function</h4>
<p>cleanScreen is what is run between hexes being clicked on, it will hide the previous text with grey boxes. It also redraws the exit and refresh buttons over those boxes.</p>

<h4>main</h4>
<p> Main is the function that calls everything we need to run. It checks what the user is doing (whether clicking on exit or a box, or a button), and if the user interacts with the program, it calls all the needed parts and will blit text to the screen for the user.</p>
