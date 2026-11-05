r"""Content of the Simple Concept notes, one entry per module, in R0 order.

Each entry: title, bigidea (one sentence), picture (a tikzpicture), idea (a
short paragraph), remember (three points) and trythis (an activity).
Pictures can use the pics defined in build_notes.py: car, scanner, tree,
house, person, satellite, imu.
"""

NOTES = [
# 1
dict(title="What Is LiDAR?",
bigidea="LiDAR measures how far away things are by timing flashes of light, just like an echo.",
picture=r"""\begin{tikzpicture}[scale=0.9]
\draw[line width=1.5pt,brown!60!black] (-7.5,0)--(7.5,0);
\pic at (-5.2,0) {house}; \pic at (5.4,0) {tree}; \pic at (0,0) {car}; \pic at (0,1.0) {scanner};
\draw[ray] (0.1,1.4)--(4.75,1.55); \draw[back] (4.75,1.15)--(0.25,1.2);
\draw[ray] (-0.1,1.4)--(-4.35,0.95);
\foreach \p in {(4.9,1.9),(5.1,1.3),(5.5,2.1),(5.8,1.6),(5.3,0.6),(-4.4,0.4),(-4.4,0.8),(-4.4,1.0),(-4.6,1.4),(-4.1,1.6)} \fill[orange] \p circle (0.09);
\node[red!80!black] at (2.9,2.0) {\lbl{flash goes out}}; \node[teal] at (3.0,0.75) {\lbl{echo comes back}};
\node[orange!80!black] at (5.6,3.1) {\lbl{each echo = one dot}};
\end{tikzpicture}""",
idea=r"""Clap your hands in a big gym and you hear an echo. A far wall sends the echo back later than a near one. A LiDAR does the same thing with tiny flashes of laser light, hundreds of thousands of times every second. Each echo becomes one dot. Millions of dots together make a 3-D picture called a \textbf{point cloud}.""",
remember=[r"The flash goes out, bounces off something, and comes back.",
          r"Every echo becomes one dot. Lots of dots make a \textbf{point cloud}.",
          r"On a moving car, we must also know where the scanner was and which way it faced for every flash."],
trythis=r"""In a gym or a big hallway, clap once and listen for the echo. Stand closer to the wall and clap again. Does the echo come back faster?"""),

# 2
dict(title="The Math Toolkit",
bigidea="A few simple math tools let us turn flashes of light into a map.",
picture=r"""\begin{tikzpicture}[scale=0.9]
\fill[orange!30] (-6,1.6) circle (1.4); \draw[line width=1pt,orange!80!black] (-6,1.6) circle (1.4);
\fill[orange] (-6,1.6) -- (-4.6,1.6) arc (0:57.3:1.4) -- cycle;
\node at (-6,-0.2) {\lbl{one slice = 1 radian}}; \node[align=center] at (-6,-0.7) {\lbl{(crust as long as the radius)}};
\draw[line width=2pt,grayx] (1.3,0)--(1.3,3.2); \draw[line width=1.5pt,brown!60!black] (-1.5,0)--(1.5,0);
\draw[line width=3pt,brown] (-0.9,0)--(1.25,2.6);
\draw[arr,teal] (-0.9,-0.35)--(1.25,-0.35); \node[teal] at (0.2,-0.75) {\lbl{across = cosine}};
\draw[arr,purple] (1.65,0)--(1.65,2.6); \node[purple,rotate=90] at (2.05,1.3) {\lbl{up = sine}};
\draw[arr,navy] (4.2,0.3)--(7.2,0.3); \draw[arr,navy] (7.2,0.3)--(7.2,1.3); \draw[arr,red!80!black,dashed] (4.2,0.3)--(7.15,1.25);
\node[navy] at (5.7,-0.1) {\lbl{3 steps east}}; \node[navy] at (7.9,0.8) {\lbl{1 north}};
\node[align=center] at (5.6,2.2) {\lbl{an arrow says}\\\lbl{how far and which way}};
\end{tikzpicture}""",
idea=r"""Big numbers get a shortcut: $10^3$ means 1 followed by 3 zeros, which is 1000. An angle can be measured in \textbf{radians}: a pizza slice whose crust is as long as the cut from the middle is one radian. Lean a stick on a wall: how far the bottom is from the wall is the \textbf{cosine}, and how high the top reaches is the \textbf{sine}.""",
remember=[r"An arrow (a \textbf{vector}) tells how far and which way.",
          r"The \textbf{average} tells where things landed. The \textbf{spread} tells how scattered they are.",
          r"A good measurement has an average right on target \emph{and} a small spread."],
trythis=r"""Throw ten crumpled paper balls at a target on the floor. Mark where they land. Where is the middle of the group? How spread out are they?"""),

# 3
dict(title="Measuring Distance with Light",
bigidea="Time the light there and back, then cut the trip in half.",
picture=r"""\begin{tikzpicture}[scale=0.9]
\fill[grayx!60] (8,0) rectangle (8.5,3.4); \node[grayx] at (8.25,3.75) {\lbl{wall}};
\fill[orange,rounded corners=3pt] (-0.6,1.1) rectangle (0.6,2.3); \fill[red!70!black] (0.6,1.7) circle (0.12);
\draw[ray,decorate,decoration={snake,amplitude=1.5pt,segment length=9pt,post length=6pt}] (0.8,2.1)--(7.9,2.1);
\draw[back,decorate,decoration={snake,amplitude=1.5pt,segment length=9pt,post length=6pt}] (7.9,1.3)--(0.8,1.3);
\node[red!80!black] at (4.3,2.6) {\lbl{1. flash goes to the wall}}; \node[teal] at (4.3,0.8) {\lbl{2. echo comes back}};
\draw[line width=1.5pt,navy,fill=white] (-2.4,1.7) circle (0.75); \draw[line width=1.5pt,navy] (-2.4,1.7)--(-2.4,2.25); \draw[line width=1.5pt,navy] (-2.4,1.7)--(-2.0,1.5);
\fill[navy] (-2.55,2.45) rectangle (-2.25,2.6); \node[navy] at (-2.4,0.6) {\lbl{stopwatch}};
\node[draw=navy,line width=1pt,rounded corners,fill=navy!5,inner sep=5pt] at (3.8,-0.4) {\lbl{distance = how far the light went, cut in half}};
\end{tikzpicture}""",
idea=r"""Light is the fastest thing there is. The LiDAR starts a stopwatch when it flashes and stops it when the echo comes back. The light went \emph{to} the wall and \emph{back}, so the wall is only half as far as the light traveled. That is why we cut the answer in half.""",
remember=[r"Light travels about 30 cm (one foot) in a billionth of a second.",
          r"The trip is there \emph{and} back, so we divide by two.",
          r"If the next flash leaves before the last echo comes home, the LiDAR can mix up which echo is which."],
trythis=r"""Shout ``Hello!'' toward a far wall or a canyon and count until you hear the echo. If you shout again before the echo comes back, can you tell which ``Hello'' you are hearing?"""),

# 4
dict(title="The Laser Beam and the Echo",
bigidea="A laser spot grows with distance, and LiDAR sees through gaps, never through solid things.",
picture=r"""\begin{tikzpicture}[scale=0.9]
\fill[grayx,rounded corners=2pt] (-1.2,1.75) rectangle (0,2.25);
\fill[gold!25] (0,1.92) -- (7,1.0) -- (7,3.0) -- (0,2.08) -- cycle;
\draw[gold!80!black,line width=1pt] (2,1.73) ellipse (0.1 and 0.25); \draw[gold!80!black,line width=1pt] (7,2.0) ellipse (0.25 and 1.0);
\node at (2,1.2) {\lbl{near: small spot}}; \node at (7,0.6) {\lbl{far: big spot}};
\draw[line width=1.5pt,brown!60!black] (9,0)--(15,0);
\fill[brown!70!black] (11.85,0) rectangle (12.15,1.6);
\foreach \x/\y in {11.2/2.3,12.0/2.8,12.8/2.3,11.5/1.8,12.5/1.8} \fill[kid!80] (\x,\y) circle (0.42);
\draw[ray] (13.9,3.6)--(12.95,0.1); \fill[orange] (12.9,0.05) circle (0.1);
\node[align=center] at (15.0,1.2) {\lbl{slips through}\\\lbl{a gap}};
\node at (12,3.7) {\lbl{leaves}};
\end{tikzpicture}""",
idea=r"""Shine a flashlight at your hand and you see a small circle. Shine it at a far wall and the circle is much bigger. A laser beam spreads too, just very slowly. Far away, the spot can be as big as a coin, so it can touch the edge of a pole and the wall behind it at the same time. The farther away something is, the dimmer its echo.""",
remember=[r"Twice as far away means only about one quarter as bright.",
          r"Shiny white things send back lots of light. Black or wet things send back very little.",
          r"LiDAR reaches the ground under trees only through gaps between the leaves. Water stops it."],
trythis=r"""In a dark room, shine a flashlight at your hand, then at a far wall. Compare the size and brightness of the spot."""),

# 5
dict(title="From Angles and Distance to X, Y, Z",
bigidea="A turn, a tilt and a distance tell you exactly where a dot is.",
picture=r"""\begin{tikzpicture}[scale=0.95]
\fill[kid!8] (-1,-0.6) -- (8,-0.6) -- (10,2) -- (1,2) -- cycle;
\draw[arr,navy] (0,0)--(7.5,0) node[right] {\lbl{X forward}};
\draw[arr,navy] (0,0)--(2.2,2.6) node[above] {\lbl{Y sideways}};
\draw[arr,navy] (0,0)--(0,4.2) node[above] {\lbl{Z up}};
\coordinate (G) at (6,1.2); \coordinate (P) at (6,3.4);
\draw[dashed,grayx,line width=1pt] (0,0)--(G); \draw[dashed,grayx,line width=1pt] (G)--(P);
\draw[ray] (0,0)--(P);
\node[star,star points=5,fill=gold,minimum size=12pt,inner sep=0] at (P) {}; \node[gold!70!black] at (6.7,3.7) {\lbl{the dot}};
\draw[teal,line width=1.4pt,-{Stealth}] (2.0,0) arc (0:11.3:2.0); \node[teal] at (2.4,-0.3) {\lbl{turn}};
\draw[purple,line width=1.4pt,-{Stealth}] (3.4,0.68) arc (11.3:29.5:3.47); \node[purple] at (4.0,1.25) {\lbl{tilt}};
\node[red!80!black,rotate=29] at (2.55,2.15) {\lbl{distance}};
\pic[scale=0.55] at (-0.5,-0.55) {person};
\end{tikzpicture}""",
idea=r"""To tell a friend where treasure is hidden, you could say: ``Face the big tree. Turn a little to the left. Look a little up. Now walk 25 steps that way.'' That is a \textbf{turn}, a \textbf{tilt} and a \textbf{distance}. A LiDAR records the same three things for every dot, then uses triangle math to change them into how far forward, how far sideways and how far up: X, Y and Z.""",
remember=[r"Every dot starts as a turn, a tilt and a distance.",
          r"X is forward, Y is sideways and Z is up.",
          r"Driving faster spreads the lines of dots farther apart on the road."],
trythis=r"""Hide a toy in the room. Guide a friend to it using only a turn, a tilt (``look up a little'') and a number of steps."""),

# 6
dict(title="Rotation, Pose and Frames",
bigidea="Pose means where you are and which way you are facing.",
picture=r"""\begin{tikzpicture}[scale=0.95]
\fill[skin,draw=orange!60!brown,line width=1pt,rounded corners=8pt] (0,0) rectangle (1.6,1.5);
\fill[skin,draw=orange!60!brown,line width=1pt,rounded corners=5pt] (1.4,0.95) rectangle (3.4,1.4);
\fill[skin,draw=orange!60!brown,line width=1pt,rounded corners=5pt] (1.4,0.35) -- (2.9,-0.45) -- (3.1,-0.1) -- (1.6,0.75) -- cycle;
\fill[skin,draw=orange!60!brown,line width=1pt,rounded corners=5pt] (0.25,1.35) rectangle (0.7,3.1);
\draw[arr,red!80!black] (3.5,1.18)--(4.9,1.18) node[right] {\lbl{X: pointer finger}};
\draw[arr,teal] (3.2,-0.3)--(4.2,-0.85) node[right] {\lbl{Y: middle finger}};
\draw[arr,navy] (0.48,3.2)--(0.48,4.3) node[above] {\lbl{Z: thumb, always up}};
\node at (1.4,-1.3) {\lbl{the right-hand rule}};
\draw[line width=1.5pt,brown!60!black] (8,-0.3)--(14,-0.3);
\pic[scale=1.3] at (11,-0.5) {car};
\draw[purple,line width=1.4pt,-{Stealth}] (9.4,2.0) arc (160:20:1.7 and 0.5); \node[purple] at (11.4,3.5) {\lbl{yaw: turn left or right}};
\draw[orange!90!black,line width=1.4pt,-{Stealth}] (14.0,0.2) arc (-40:60:0.5 and 1.0); \node[orange!90!black,align=center] at (15.4,1.0) {\lbl{pitch:}\\\lbl{nose up/down}};
\draw[kid,line width=1.4pt,-{Stealth}] (8.6,1.4) arc (130:230:0.45 and 0.9); \node[kid,align=center] at (8.6,2.9) {\lbl{roll: lean}\\\lbl{side to side}};
\end{tikzpicture}""",
idea=r"""Stand in the middle of a room. Where you are is your spot on the floor. Which way you face is whether you look at the board or the window, and whether you tilt or lean. A LiDAR on a car needs to know both, all the time, because the car bumps, turns and leans. Together they are called its \textbf{pose}.""",
remember=[r"Pose = where you are + which way you are facing.",
          r"Right hand: pointer finger is X, middle finger is Y, and the thumb is always Z.",
          r"Roll is leaning, pitch is nose up or down, and yaw is turning left or right."],
trythis=r"""Hold up your right hand: pointer finger forward, middle finger to the left, thumb up. Now turn your hand to show roll, pitch and yaw."""),

# 7
dict(title="The IMU: Feeling Motion",
bigidea="An IMU feels every push and turn, but its guess slowly drifts.",
picture=r"""\begin{tikzpicture}[scale=0.95]
\fill[purple!15,draw=purple,line width=1.5pt,rounded corners=4pt] (-1.2,0.4) rectangle (1.2,2.4); \node[purple] at (0,1.4) {\Large\bfseries IMU};
\draw[arr,red!80!black] (1.3,1.4)--(2.6,1.4); \draw[arr,red!80!black] (0,2.5)--(0,3.6); \draw[arr,red!80!black] (-1.3,0.6)--(-2.3,-0.2);
\node[red!80!black] at (2.2,3.4) {\lbl{3 push-feelers}};
\draw[teal,line width=1.4pt,-{Stealth}] (-1.9,2.3) arc (200:340:0.55 and 0.25); \draw[teal,line width=1.4pt,-{Stealth}] (1.9,0.2) arc (200:340:0.55 and 0.25);
\draw[teal,line width=1.4pt,-{Stealth}] (-2.2,1.0) arc (110:250:0.25 and 0.4);
\node[teal] at (-2.4,3.0) {\lbl{3 spin-feelers}};
\draw[kid,line width=2pt,dashed] (5,0.5)--(13,0.5); \node[kid] at (12.4,0.1) {\lbl{real path}};
\draw[red!80!black,line width=2pt] (5,0.5) .. controls (8,0.5) and (10.5,1.2) .. (13,2.6); \node[red!80!black] at (11.0,2.6) {\lbl{IMU's guess}};
\pic at (5,0.1) {car};
\draw[decorate,decoration={brace,amplitude=6pt},line width=1pt] (13.3,2.6)--(13.3,0.5); \node[align=center] at (14.4,1.55) {\lbl{grows}\\\lbl{over time}};
\end{tikzpicture}""",
idea=r"""When a car speeds up, you get pushed back into your seat. When it turns, you lean to the side. You feel the motion even with your eyes closed. An IMU is a little box that feels motion the same way. By adding up all those feelings many times a second, it can guess where the car went, even inside a tunnel. But like walking with your eyes closed, the guess slowly gets worse.""",
remember=[r"An IMU has three push-feelers and three spin-feelers.",
          r"It adds up thousands of tiny readings, so tiny mistakes add up too.",
          r"That is why the IMU needs help from GPS or the laser to stay on track."],
trythis=r"""In an open, safe space, with a friend watching, close your eyes and walk 10 steps toward a spot, turn around and walk back. How far from the start did you end up?"""),

# 8
dict(title="Timing, GNSS and Motion Compensation",
bigidea="Every sensor must share one clock, and GPS and the IMU make a perfect team.",
picture=r"""\begin{tikzpicture}[scale=0.92]
\draw[line width=2pt,navy,fill=white] (0,3.3) circle (0.8); \draw[line width=2pt,navy] (0,3.3)--(0,3.85); \draw[line width=2pt,navy] (0,3.3)--(0.4,3.1);
\node[navy] at (0,4.4) {\lbl{one clock}};
\pic at (-2.6,0.8) {scanner}; \node at (-2.6,0.3) {\lbl{laser}};
\pic at (0,1.0) {imu};
\fill[grayx,rounded corners=2pt] (2.2,0.8) rectangle (3.0,1.3); \fill[white] (2.6,1.05) circle (0.15); \node at (2.6,0.3) {\lbl{camera}};
\draw[line width=1pt,navy,dashed] (-0.6,2.75)--(-2.5,1.3); \draw[line width=1pt,navy,dashed] (0,2.5)--(0,1.35); \draw[line width=1pt,navy,dashed] (0.6,2.75)--(2.5,1.4);
\draw[line width=1.5pt,brown!60!black] (5.5,0)--(15,0);
\pic at (7,3.8) {satellite}; \draw[gold!80!black,line width=1.3pt,decorate,decoration={snake,amplitude=2pt,segment length=8pt}] (7,3.4)--(7.3,1.2);
\pic at (7.4,0) {car}; \node at (7.4,-0.55) {\lbl{GPS works}};
\fill[grayx!50] (11,0) -- (11,1.7) arc (180:0:1.7 and 1.1) -- (14.4,0) -- (13.6,0) -- (13.6,1.7) arc (0:180:0.9 and 0.5) -- (11.8,0) -- cycle;
\pic[scale=0.7] at (12.7,0) {car};
\draw[gold!80!black,line width=1.3pt,decorate,decoration={snake,amplitude=2pt,segment length=8pt}] (11.7,4.0)--(12.5,3.0); \node[red!80!black] at (12.6,2.85) {\Large\bfseries$\times$};
\node[align=center] at (12.7,-0.65) {\lbl{tunnel: the IMU carries on}};
\end{tikzpicture}""",
idea=r"""If your camera's clock is one second slow, your photo of a runner crossing the finish line gets labeled at the wrong time, and the runner seems to be in the wrong place. Every sensor on a mapping car must use the \emph{same} clock, set perfectly, so every laser dot is matched to exactly where the car was at that instant.""",
remember=[r"One clock for the laser, the IMU, the camera and GPS.",
          r"GPS never drifts but can disappear. The IMU never stops but drifts. Together they are great.",
          r"The car moves while the laser spins, so each dot is moved back to where it really was (\textbf{de-skewing})."],
trythis=r"""Take a photo of something moving fast, like a ball being thrown. Is it blurry? The LiDAR has the same problem and fixes it by using the time of every dot."""),

# 9
dict(title="Lever Arm and Boresight Calibration",
bigidea="We must measure exactly how far apart, and how twisted, the sensors are.",
picture=r"""\begin{tikzpicture}[scale=1.0]
\fill[grayx!40,rounded corners=3pt] (-1,0) rectangle (9,0.45); \node[grayx] at (4,-0.35) {\lbl{one solid plate}};
\pic[scale=1.6] at (0.6,0.85) {imu};
\begin{scope}[shift={(7.4,0.45)},rotate=8]
\fill[orange,rounded corners=3pt] (-0.5,0) rectangle (0.5,1.4); \fill[red!70!black] (0,1.4) circle (0.2); \node[white] at (0,0.7) {\lbl{laser}};
\draw[dashed,red!80!black,line width=1pt] (0,1.4)--(0,3.2);
\end{scope}
\draw[dashed,grayx,line width=1pt] (7.35,1.85)--(7.35,3.65);
\draw[purple,line width=1.4pt,-{Stealth}] (7.35,3.2) arc (90:98:3.0); \node[purple,align=left,right] at (8.2,2.7) {\lbl{boresight:}\\\lbl{how much it is twisted}};
\draw[<->,line width=1.6pt,teal,>={Stealth[length=8pt]}] (1.4,1.6)--(6.8,1.6); \node[teal] at (4.1,2.0) {\lbl{lever arm: how far apart}};
\end{tikzpicture}""",
idea=r"""Put a toy camera on your shoulder and close your eyes. You know where \emph{you} are, but the camera is a little to the side, a little higher, and maybe turned a bit. Forget that, and you point to the wrong place. On a mapping car the motion sensor (the IMU) and the laser are in different spots too.""",
remember=[r"The \textbf{lever arm} is how far apart the sensors are.",
          r"The \textbf{boresight} is how much one is twisted compared with the other.",
          r"Check them again after the mount is bumped, moved or stored for a long time."],
trythis=r"""Tape a straw to the side of a box so it points a little off to one side. Aim the box at a target. Where does the straw really point?"""),

# 10
dict(title="SLAM: Mapping While Finding Yourself",
bigidea="SLAM draws the map and finds where you are on it, a little at a time.",
picture=r"""\begin{tikzpicture}[scale=0.95]
\node[star,star points=5,fill=gold,minimum size=16pt,inner sep=0] (S) at (0,0) {}; \node[gold!70!black] at (0,-0.6) {\lbl{start}};
\draw[red!80!black,line width=2pt,dashed] (0,0) -- (6,0) -- (6.4,3.2) -- (0.8,3.9) -- (1.3,1.2);
\fill[red!80!black] (1.3,1.2) circle (0.12); \node[red!80!black,align=center] at (2.9,1.3) {\lbl{guess drifted:}\\\lbl{does not close}};
\draw[teal,line width=2pt] (0,0) -- (6,0) -- (6,3.4) -- (0,3.4) -- (0,0.25);
\node[teal,align=center] at (3,4.4) {\lbl{saw the start again: fix the whole map}};
\pic[scale=0.6] at (6.9,0.1) {person};
\draw[line width=1.5pt,navy] (9.5,0.3) rectangle (15,3.6); \draw[line width=1.5pt,navy] (12,0.3)--(12,2.2); \draw[line width=1.5pt,navy] (9.5,2.2)--(11,2.2);
\fill[navy] (10.3,1.2) circle (0.18); \draw[line width=1pt,navy,dashed] (10.3,1.2) circle (0.7);
\node[navy,align=center] at (12.3,-0.3) {\lbl{step, feel a wall, add it to the map}};
\end{tikzpicture}""",
idea=r"""You are blindfolded in a new house and must draw a map. To draw a wall in the right place, you need to know where you are. But to know where you are, you need a map! SLAM does both a little at a time: take a step, feel a wall, guess where you are, add the wall to your map. When you bump into a wall you already drew, you fix up your whole map.""",
remember=[r"\textbf{SLAM} = making the map and finding yourself on it, at the same time.",
          r"Moving makes you less sure. Seeing something you know makes you more sure.",
          r"Coming back to the start (a \textbf{loop closure}) fixes the whole path, like closing a traverse."],
trythis=r"""Walk around your room once while drawing a map of it. When you get back to the door, does your drawing meet up? Fix it so it does."""),

# 11
dict(title="Scan Matching: Fitting Clouds Together",
bigidea="Slide and twist the new scan until it lines up with the old one.",
picture=r"""\begin{tikzpicture}[scale=0.95]
\draw[navy,line width=2.5pt] (0,3.2)--(0,0)--(4,0)--(4,1.6)--(2.2,1.6)--(2.2,3.2);
\begin{scope}[shift={(1.1,0.6)},rotate=12]
\draw[red!80!black,line width=2.5pt,dashed] (0,3.2)--(0,0)--(4,0)--(4,1.6)--(2.2,1.6)--(2.2,3.2);
\end{scope}
\draw[arr,teal] (6.6,2.6) arc (60:120:1.6); \node[teal,align=center] at (6.4,3.7) {\lbl{slide and twist}\\\lbl{until they match}};
\node[navy] at (1.0,-0.45) {\lbl{old scan}}; \node[red!80!black] at (5.6,-0.1) {\lbl{new scan}};
\draw[line width=2pt,grayx] (8.5,0.4)--(15,0.4); \draw[line width=2pt,grayx] (8.5,2.6)--(15,2.6);
\draw[<->,line width=1.5pt,orange!90!black,>={Stealth[length=8pt]}] (10,1.5)--(13.5,1.5);
\node[align=center] at (11.75,3.4) {\lbl{a plain hallway:}}; \node[align=center] at (11.75,-0.3) {\lbl{every spot looks the same}};
\node[orange!90!black] at (11.75,1.95) {\lbl{which spot?}};
\end{tikzpicture}""",
idea=r"""Draw a shape on a see-through sheet. A friend draws the same shape on another sheet, a little shifted and turned. Lay one sheet on the other and slide and twist the top one until the drawings line up. How far you slid and twisted it tells you how your friend's sheet was placed. A LiDAR does this with two scans to learn how far the car moved.""",
remember=[r"Matching two scans tells how far the scanner moved and turned.",
          r"Sharp corners and flat walls are the easiest things to match.",
          r"In a long, plain hallway everything looks alike, so add targets or cross the hallway."],
trythis=r"""Trace a shape on two sheets of tracing paper. Shift and turn one, then slide it back until the shapes match."""),

# 12
dict(title="Factor Graphs and LIO-SAM",
bigidea="Every measurement is a rubber band, and the map settles where the pulling is shared fairly.",
picture=r"""\begin{tikzpicture}[scale=1.0]
\fill[brown!60!black] (-0.35,-0.2) rectangle (0.35,2.4); \node[brown!60!black,align=center] at (0,-0.7) {\lbl{a post:}\\\lbl{``you belong here''}};
\foreach \i in {1,...,5} {\pic[scale=0.75] at (2.4*\i,0.4) {person};}
\draw[gold!80!black,line width=2pt,decorate,decoration={coil,aspect=0.5,segment length=6pt,amplitude=4pt}] (0.35,1.6)--(2.15,1.55);
\foreach \i in {1,...,4} {\draw[gold!80!black,line width=2pt,decorate,decoration={coil,aspect=0.5,segment length=6pt,amplitude=4pt}] (2.4*\i+0.3,1.55)--(2.4*\i+2.1,1.55);}
\node[gold!70!black] at (7.2,2.6) {\lbl{rubber bands = measurements}};
\node[navy] at (7.2,-0.3) {\lbl{people = where the car was, moment by moment}};
\end{tikzpicture}""",
idea=r"""Picture a row of people joined by rubber bands. Each band says ``you two should be this far apart.'' One person is also tied to a post that says ``you belong here.'' If one band pulls a little wrong, everyone wiggles until the pulling is shared out as fairly as possible. That picture is a \textbf{factor graph}: the people are the car's positions over time, and the bands are measurements.""",
remember=[r"Each measurement pulls a little on the positions it connects.",
          r"GPS is like the post: it ties the path to the real world.",
          r"The finished path, with direction at every instant, is called the \textbf{trajectory}."],
trythis=r"""Link four or five rubber bands into a chain and pin one end down. Pull the other end and watch how the stretch spreads along the whole chain."""),

# 13
dict(title="Control, Error Budgets and Accuracy Standards",
bigidea="Control points pin the map to the real world, and secret checkpoints test it.",
picture=r"""\begin{tikzpicture}[scale=0.95]
\fill[kid!8,draw=kid,line width=1.5pt,rounded corners=4pt] (0,0) rectangle (8,4);
\foreach \x in {1.5,4,6.5} \fill[grayx!35] (\x-0.7,0.6) rectangle (\x+0.7,1.6);
\fill[grayx!35] (2.5,2.4) rectangle (5.5,3.4); \node at (2.0,4.4) {\lbl{the LiDAR map}};
\foreach \p in {(0.5,0.4),(7.5,0.4),(4,3.7),(0.5,3.6)} {\fill[red!80!black] \p ++(0,0.5) -- ++(-0.2,0) -- ++(0.2,-0.5) -- ++(0.2,0.5) -- cycle; \fill[red!80!black] \p ++(0,0.62) circle (0.16);}
\foreach \p in {(2.7,1.95),(6,2.6),(5.3,0.4)} {\draw[navy,line width=1.3pt] \p circle (0.25); \draw[navy,line width=1.3pt] \p circle (0.1);}
\fill[red!80!black] (9.2,3.0) -- ++(-0.2,0) -- ++(0.2,-0.5) -- ++(0.2,0.5) -- cycle; \fill[red!80!black] (9.2,3.12) circle (0.16);
\node[right,red!80!black] at (9.6,2.9) {\lbl{control point: pins the map in place}};
\draw[navy,line width=1.3pt] (9.2,1.5) circle (0.25); \draw[navy,line width=1.3pt] (9.2,1.5) circle (0.1);
\node[right,navy,align=left] at (9.6,1.5) {\lbl{checkpoint: kept secret,}\\\lbl{used only to test the map}};
\end{tikzpicture}""",
idea=r"""You can draw a perfect map of your bedroom, with every toy in the right place compared with every other toy. But if you don't know where your house is on the street, nobody else can use it to find your room. SLAM makes the bedroom map. \textbf{Control points}, measured very carefully by surveyors, pin that map onto the real world.""",
remember=[r"A map can look perfect and still be in the wrong place.",
          r"\textbf{Checkpoints} are kept secret from the computer and used only to test the map.",
          r"A formal test uses at least 30 checkpoints, spread over the whole project."],
trythis=r"""Draw a map of your room. Pick three spots and measure them with a tape measure. Does your map agree with the tape?"""),

# 14
dict(title="Error Propagation and Error Budgets",
bigidea="Every small mistake adds a little, and we add them up to see the whole.",
picture=r"""\begin{tikzpicture}[scale=0.95]
\foreach \x/\t in {0/random,5/systematic,10/blunder} {
  \foreach \r/\c in {1.5/white,1.1/red!25,0.7/white,0.3/red!60} \fill[\c,draw=grayx] (\x,2) circle (\r);
  \node at (\x,-0.1) {\lbl{\t}}; }
\foreach \p in {(-0.9,2.6),(0.6,1.2),(0.9,2.9),(-0.5,1.0),(0.2,2.4),(-1.0,1.7)} \fill[navy] \p circle (0.1);
\foreach \p in {(4.0,2.7),(4.2,2.9),(3.9,2.95),(4.15,2.55),(3.8,2.6)} \fill[navy] \p circle (0.1);
\foreach \p in {(10.1,2.1),(9.8,1.8),(10.3,2.3),(9.9,2.4)} \fill[navy] \p circle (0.1);
\fill[red!80!black] (12.1,3.6) circle (0.12); \node[red!80!black] at (12.5,3.95) {\lbl{hit the wall!}};
\node[align=center,grayx] at (0,-0.6) {\lbl{shaky hand}}; \node[align=center,grayx] at (5,-0.6) {\lbl{crooked board}}; \node[align=center,grayx] at (10,-0.6) {\lbl{one big slip}};
\end{tikzpicture}""",
idea=r"""Throw darts. If they land all over, that is \textbf{random error}: your hand shakes a little differently each time. If they land in a tight group but always to one side, that is \textbf{systematic error}: maybe the board is crooked. If one dart hits the wall, that is a \textbf{blunder}. Each one is fixed in a different way.""",
remember=[r"Practice shrinks random error. Fixing the cause removes systematic error. Blunders are thrown out.",
          r"An \textbf{error budget} lists every little thing that can move a dot, like packing a backpack.",
          r"Averaging many tries shrinks random error, but it cannot fix a crooked board."],
trythis=r"""Throw five paper balls at a target. Then tilt the target a little and throw five more. Which group is spread out, and which is shifted?"""),

# 15
dict(title="Ouster OS0 Case Study: Errors and Resolution",
bigidea="Small marks, steady answers and a true ruler are three different things.",
picture=r"""\begin{tikzpicture}[scale=0.95]
\fill[gold!25,draw=gold!80!black,line width=1pt] (0,2.6) rectangle (10,3.5);
\foreach \i in {0,...,40} {\draw[line width=0.6pt] (\i/4,3.5)--(\i/4,3.25);}
\foreach \i in {0,...,10} {\draw[line width=1pt] (\i,3.5)--(\i,3.0);}
\node[right,align=left] at (10.3,3.05) {\lbl{resolution:}\\\lbl{how small the marks are}};
\fill[gold!25,draw=gold!80!black,line width=1pt] (0,0.9) rectangle (10.8,1.8);
\foreach \i in {0,...,10} {\draw[line width=1pt] (\i*1.08,1.8)--(\i*1.08,1.3);}
\node[red!80!black,right,align=left] at (11.1,1.35) {\lbl{accuracy: is the ruler}\\\lbl{the right length? (stretched!)}};
\foreach \x/\y in {4.6/0.2,4.85/0.3,5.0/0.12,5.2/0.28,5.35/0.18,4.75/0.05} \fill[navy] (\x,\y) circle (0.1);
\node[navy,right,align=left] at (5.6,0.15) {\lbl{precision: how much your answers wiggle}};
\end{tikzpicture}""",
idea=r"""A datasheet is like the label on a box of crayons: it tells how many colors, how sharp the tips are and how long they last. To know whether you can draw a tiny ant or only a big elephant, you do a little math with those numbers. That is what this module does for one real laser scanner.""",
remember=[r"\textbf{Resolution} is how small the marks are.",
          r"\textbf{Precision} is how much your answer wiggles if you measure the same thing ten times.",
          r"\textbf{Accuracy} is whether the ruler itself is the right length. Tiny marks can still be on a stretched ruler!"],
trythis=r"""Measure the width of a book five times with a ruler. Write each answer down. How much do they wiggle?"""),

# 16
dict(title="Choosing an IMU: AHRS, GNSS/INS and Tactical GNSS/INS",
bigidea="A step-counter alone drifts; ``you are here'' messages keep you on track.",
picture=r"""\begin{tikzpicture}[scale=0.95]
\fill[grayx!25] (0,0) rectangle (5,4); \fill[white] (0.5,0.5) rectangle (4.5,3.5);
\foreach \p in {(0.9,0.9),(4.1,0.9),(4.1,3.1),(0.9,3.1)} \fill[kid!70] \p circle (0.25);
\draw[red!80!black,line width=2pt,dashed] (0.25,0.25) -- (4.85,0.45) -- (5.3,4.4) -- (0.9,4.9) -- (0.75,1.0);
\draw[teal,line width=2pt] (0.25,0.25) -- (4.75,0.25) -- (4.75,3.75) -- (0.25,3.75) -- (0.25,0.4);
\node[star,star points=5,fill=gold,minimum size=14pt,inner sep=0] at (0.25,0.25) {};
\node[red!80!black,right,align=left] at (6,3.6) {\lbl{compass and step-counter only:}\\\lbl{drifts away}};
\node[teal,right,align=left] at (6,2.1) {\lbl{plus ``you are here'' messages:}\\\lbl{stays on the block}};
\fill[navy,rounded corners=2pt] (6.3,0.1) rectangle (6.9,1.1); \fill[white] (6.38,0.3) rectangle (6.82,0.95);
\draw[navy,line width=1pt] (7.1,0.9) arc (-30:30:0.3); \draw[navy,line width=1pt] (7.35,0.8) arc (-30:30:0.5);
\node[right] at (7.9,0.6) {\lbl{RTK: give or take 2 cm}};
\end{tikzpicture}""",
idea=r"""Imagine two friends walking around the block with their eyes closed. The first has a compass and counts steps. The second has the same compass and step-counter but also gets a phone message every second saying ``you are about here.'' Who gets home closest? With very good messages, the second friend can walk the block and point to the mailbox almost perfectly.""",
remember=[r"A compass and step-counter alone slowly drift off course.",
          r"``You are here'' messages from GPS stop the drift.",
          r"Steel, motors and bridges can fool a magnetic compass, so keep it away from them."],
trythis=r"""Walk once around a table counting steps, then try it with your eyes closed and a friend calling out ``you're at the corner'' at each corner. Which way ends up closer?"""),

# 17
dict(title="Survey-Grade Case Study: RIEGL VUX-240",
bigidea="With a top scanner, the biggest mistake is often where the airplane is.",
picture=r"""\begin{tikzpicture}[scale=0.95]
\begin{scope}[shift={(2.5,3.6)}]
\fill[grayx] (-1.4,-0.15) rectangle (1.4,0.15); \fill[grayx] (1.4,-0.15) -- (1.8,0.35) -- (1.4,0.15) -- cycle;
\fill[grayx] (-0.3,0.1) -- (0.2,0.9) -- (0.5,0.1) -- cycle; \fill[grayx] (-0.3,-0.1) -- (0.2,-0.9) -- (0.5,-0.1) -- cycle;
\end{scope}
\foreach \x in {0,1,...,5} \draw[red!70!black,line width=0.8pt] (2.5,3.4)--(\x,0.1);
\draw[line width=1.5pt,brown!60!black] (-0.5,0)--(5.5,0); \foreach \x in {0,1,...,5} \fill[orange] (\x,0.05) circle (0.09);
\node at (2.5,-0.45) {\lbl{500 ft below}};
\fill[navy!50] (8,0) rectangle (9.2,0.8); \node[right] at (9.4,0.4) {\lbl{laser wobble}};
\fill[purple!50] (8,0.8) rectangle (9.2,1.9); \node[right] at (9.4,1.35) {\lbl{tilt and turn sensor}};
\fill[red!60] (8,1.9) rectangle (9.2,3.6); \node[right] at (9.4,2.75) {\lbl{airplane's GPS position}};
\node at (8.6,4.1) {\lbl{the mistakes, stacked}};
\end{tikzpicture}""",
idea=r"""This scanner is a super-fast, super-careful version of the ones we met before. It fires up to 2.4 million laser flashes a second from an airplane. To know where each dot lands 500 feet below, we add up all the little mistakes: the laser's own wobble, the tiny tilt and turn errors of the motion sensor, and where GPS thinks the airplane is.""",
remember=[r"The farther away the ground, the more a tiny tilt moves each dot.",
          r"With a scanner this good, the laser is no longer the weak link.",
          r"Great results come from the whole system, not from the laser alone."],
trythis=r"""Stack building blocks, one for each mistake: a small one for the laser, a medium one for tilt, a big one for GPS. Which block makes the stack tallest?"""),

# 18
dict(title="Processing, QA/QC and Deliverables",
bigidea="Clean the cloud: throw out lonely dots, and keep one dot per box.",
picture=r"""\begin{tikzpicture}[scale=0.95]
\foreach \i in {1,...,45} \fill[navy] ({1.8+0.9*rand},{1.8+0.8*rand}) circle (0.07);
\fill[red!80!black] (5.2,3.6) circle (0.1); \draw[red!80!black,line width=1.5pt] (4.9,3.3)--(5.5,3.9) (4.9,3.9)--(5.5,3.3);
\node[red!80!black,align=center] at (5.2,2.7) {\lbl{lonely dot:}\\\lbl{dust or a bird}};
\node at (2.2,0.3) {\lbl{the crowd stays}};
\draw[grayx,line width=1pt] (8,0.6) grid[step=1.2] (12.8,3.0);
\foreach \i in {1,...,40} \fill[navy!40] ({10.4+2.3*rand},{1.8+1.15*rand}) circle (0.05);
\foreach \x in {8.6,9.8,11.0,12.2} \foreach \y in {1.2,2.4} \fill[teal] (\x,\y) circle (0.13);
\node[align=center] at (10.4,0.05) {\lbl{each box keeps one dot}};
\node[align=center,red!80!black] at (10.4,3.55) {\lbl{boxes too big lose the curb!}};
\end{tikzpicture}""",
idea=r"""Picture a crowd standing close together in a park, except one person way out by the fence. You can tell that person is alone because their nearest neighbors are far away. Cleaning a point cloud works the same way: dots whose neighbors are far away are usually dust, rain, birds or reflections, so they are thrown out.""",
remember=[r"Lonely dots are removed (\textbf{outlier removal}).",
          r"Thinning keeps one dot per little box. Boxes that are too big round off curbs and edges.",
          r"Ground dots are sorted out to build the bare-earth surface."],
trythis=r"""Spread a handful of beans on a table and push one far away. Which bean is the ``lonely dot''? Now draw a grid and keep just one bean in each square."""),

# 19
dict(title="Florida Standards of Practice, FDOT and the New Datums",
bigidea="The scanner is a new measuring tape, but the same rulebook still applies.",
picture=r"""\begin{tikzpicture}[scale=0.95]
\fill[navy,rounded corners=3pt] (0,0.3) rectangle (2.6,3.6); \fill[white] (2.6,0.45) rectangle (2.8,3.45);
\node[white,align=center] at (1.3,2.3) {\bfseries RULE}; \node[white,align=center] at (1.3,1.7) {\bfseries BOOK};
\fill[kid!8,draw=kid,line width=1.5pt,rounded corners=3pt] (5,0.3) rectangle (10,3.6);
\draw[grayx,line width=1pt] (5.5,1.0) -- (7,2.8) -- (9.4,2.4); \draw[grayx,line width=1pt] (6.2,0.6) -- (8.5,1.4);
\draw[red!80!black,line width=2pt] (8.8,1.1) circle (0.55); \node[red!80!black] at (8.8,1.1) {\lbl{SEAL}};
\node at (7.5,3.95) {\lbl{the signed map}};
\draw[arr,teal] (2.9,1.95)--(4.9,1.95); \node[teal,align=center] at (3.9,2.6) {\lbl{same rules}};
\node[align=left,right] at (10.5,2.6) {\lbl{say which datum,}};
\node[align=left,right] at (10.5,2.0) {\lbl{which foot,}};
\node[align=left,right] at (10.5,1.4) {\lbl{and how it was checked}};
\end{tikzpicture}""",
idea=r"""Every game has a rulebook. Surveyors in Florida have one too, written by the state. It says what every map must show, how accurate it must be, how you prove it, and how you sign your name to it. When the map is made with a laser scanner instead of a total station, the rulebook still applies.""",
remember=[r"Accuracy must be checked by points the computer never used.",
          r"Always label which datum and which foot the numbers use. A mix-up moves every point.",
          r"New national datums are coming, so keep the data needed to move the map onto them later."],
trythis=r"""Write the rules for a simple game you know. What does every player have to do before their score counts?"""),

# 20
dict(title="Professional Practice for LiDAR Surveys",
bigidea="A great scanner doesn't make a professional; careful habits do.",
picture=r"""\begin{tikzpicture}[scale=0.95]
\fill[brown!50,rounded corners=4pt] (0,0) rectangle (7.2,4.4); \fill[white] (0.4,0.3) rectangle (6.8,3.9);
\fill[grayx] (2.8,4.1) rectangle (4.4,4.6);
\foreach \t [count=\i] in {right person in charge,write down the promise,work safely,keep the originals,sign only what you checked} {
  \node[kid] at (1.0,4.05-\i*0.68) {\large$\checkmark$}; \node[right] at (1.4,4.05-\i*0.68) {\lbl{\t}}; }
\fill[orange] (10,0) -- (10.6,3.0) -- (11.2,0) -- cycle; \fill[white] (10.25,1.1) rectangle (10.95,1.5); \fill[white] (10.42,2.1) rectangle (10.78,2.4);
\fill[orange!80!black] (9.4,0) rectangle (11.8,0.25); \node at (10.6,-0.4) {\lbl{safety first}};
\end{tikzpicture}""",
idea=r"""Having a great camera doesn't make you a professional photographer. A professional also makes sure the right person is in charge, writes down what was promised, works safely, keeps the originals and signs only what they have checked. The same is true for a laser scanner.""",
remember=[r"Agree on what will be delivered, and how accurate it must be, before you start.",
          r"Keep the original data. It is the proof of what you measured.",
          r"Only sign for work you have checked yourself."],
trythis=r"""Make a checklist for a job you do at home, like packing for a trip. Check each item off as you go. Did the list catch anything you would have forgotten?"""),

# 21
dict(title="Capstone and Sample Project Dataset",
bigidea="Measure carefully, control what you can, check what you must, and write down what you did.",
picture=r"""\begin{tikzpicture}[scale=0.95]
\fill[grayx!35] (0,0.6) rectangle (15,1.6); \foreach \x in {0.4,1.6,...,14.8} \fill[white] (\x,1.05) rectangle (\x+0.6,1.15);
\foreach \x/\c/\t [count=\i] in {1.5/red!80!black/measure,4.5/teal/control,7.5/navy/check,10.5/purple/document,13.5/gold!80!black/trust the map} {
  \fill[\c] (\x,2.6) circle (0.55); \node[white] at (\x,2.6) {\large\bfseries\i}; \node[\c] at (\x,3.5) {\lbl{\t}}; }
\foreach \x in {2.2,5.2,8.2,11.2} \draw[arr,grayx] (\x,2.6)--(\x+0.6,2.6);
\pic at (1.5,0.45) {car}; \pic at (1.5,1.45) {scanner};
\node[align=center] at (7.5,0.0) {\lbl{one road, every skill from the course}};
\end{tikzpicture}""",
idea=r"""This is the ``big game'' at the end of the season. You use every skill you practiced: measuring with light, turning angles into dots, keeping track of the car, fixing mistakes with landmarks, and checking your work with secret checkpoints. If every step is done carefully, the final map can be trusted to build a real road.""",
remember=[r"Read the trajectory first. It shows where the map is strong and where it is weak.",
          r"Put extra checkpoints where the map is weakest, like under a bridge.",
          r"Write down what you did, so someone else could check it."],
trythis=r"""Plan a pretend survey of your yard or school playground. Where would you put control points? Where would you put secret checkpoints to test your map?"""),
]
