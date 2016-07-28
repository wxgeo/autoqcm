from string import ascii_letters

SQUARE_SIZE_IN_CM = 0.25
CELLULAR_SIZE_IN_CM = 0.5

def generate_tex(identifier=0, questions=(), answers=None):
    """Generate a tex file to be scanned later.

    identifier is the integer which identifies the sheet.

    questions is either a list (or any iterable) of questions numbers,
    or an integer n (questions number will be automatically generated then:
    1, 2, 3, ..., n).

    answer is either a list (or any iterable) of questions numbers,
    or an integer n≤26 (answers identifiers will be automatically generated then:
    a, b, c, ...).
    """
    with open("test.tex", "w") as f:
        # Header
        f.write(r"""
\documentclass[a4paper,10pt]{article}
\usepackage[utf8]{inputenc}
\usepackage{tikz}
\usepackage[left=1cm,right=1cm,top=1cm,bottom=1cm]{geometry}
\parindent=0cm
\newcommand{\tikzscale}{.5}
\begin{document}
""")
        # Two top squares to calibrate and identification band between them

        # Top left square.
        f.write(r"""
\begin{{tikzpicture}}[scale={scale}]
 \draw[fill=black] (0,0) rectangle (1,1);
\end{{tikzpicture}}""".format(scale=SQUARE_SIZE_IN_CM))

        # Identification band
        n = identifier
        f.write(r"""\hfill
\begin{{tikzpicture}}[scale={scale}]
\draw[fill=black] (-1,0) rectangle (0,1);
""".format(scale=SQUARE_SIZE_IN_CM))
        for i in range(15):
            f.write(r"""\draw[fill={color}] ({x1},0) rectangle ({x2},1);
""".format(color=("black" if n%2 else "white"), x1=i, x2=i+1))
            n = n//2

        f.write(r"""\end{tikzpicture}
\hfill
""")

        # Top right square.
        f.write(r"""\begin{{tikzpicture}}[scale={scale}]
 \draw[fill=black] (0,0) rectangle (1,1);
\end{{tikzpicture}}
""".format(scale=SQUARE_SIZE_IN_CM))

        # Header delimiter.

        f.write(r"""

\vspace{-1em}
\begin{scriptsize}\hfill\textsc{Ne rien écrire ci-dessus.}\hfill\hfill\hfill\textsc{Ne rien écrire ci-dessus.}\hfill\hfil\end{scriptsize}
\smallskip

\hrule

""")

        # Generate the table where students will answer
        scale = CELLULAR_SIZE_IN_CM
        f.write(r"""
\begin{{center}}
\begin{{tikzpicture}}[scale={scale}]
\draw[fill=black] (-1,0) rectangle (0,1);
""".format(**locals()))

        if isinstance(questions, int):
            questions = range(1, questions + 1)

        # Not all iterables have a .__len__() method, so calculate it.
        n = 0

        for x1, name in enumerate(questions):
            x2=x1 + 1
            x3=.5*(x1 + x2)
            f.write(r"""\draw ({x1},0) rectangle ({x2},1) ({x3},0.5) node {{{name}}};
""".format(**locals()))
            n += 1

        if isinstance(answers, int):
            answers = ascii_letters[:answers]

        for i, name in enumerate(answers):
            y1 = -i
            y2 = y1 - 1
            y3 = .5*(y1 + y2)
            f.write(r"""
\draw (-1,{y1}) rectangle (0,{y2}) (-0.5,{y3}) node {{{name}}};
""".format(**locals()))
            for x1 in range(n):
                x2=x1 + 1
                f.write(r"""\draw ({x1},{y1}) rectangle ({x2},{y2});
""".format(**locals()))


        f.write(r"""
\end{tikzpicture}
\end{center}
""")

        # That's all folks !
        f.write(r"\end{document}")




generate_tex(identifier=1+4+16+128+1024,
             questions=["A1","A2","B1","B2","C"],
             answers=5,
                       )
