from string import ascii_letters
import csv

SQUARE_SIZE_IN_CM = 0.25
CELL_SIZE_IN_CM = 0.5

def generate_tex(filename, identifier=0, questions=(), answers=None, options={}, _n_student=None):
    """Generate a tex file to be scanned later.

    filename is a filename without extension.

    identifier is the integer which identifies the sheet.

    questions is either a list (or any iterable) of questions numbers,
    or an integer n (questions number will be automatically generated then:
    1, 2, 3, ..., n).

    answers is either a list (or any iterable) of questions numbers,
    or an integer n≤26 (answers identifiers will be automatically generated then:
    a, b, c, ...).

    options is a dict keys are tuples (column, line) and values are tikz options
    to be passed to corresponding cell in the table for answers.

    _n_student is for test purpose only (select a student number).
    """

    if filename.endswith(".tex"):
        filename = filename[:-4]

    with open("%s.tex" % filename, "w") as f:
        # Header
        f.write(r"""
            \documentclass[a4paper,10pt]{article}
            \usepackage[utf8]{inputenc}
            \usepackage{tikz}
            \usepackage[left=1cm,right=1cm,top=1cm,bottom=1cm]{geometry}
            \parindent=0cm
            \newcommand{\tikzscale}{.5}
            \makeatletter
            \newcommand{\simfill}{%
            \leavevmode \cleaders \hb@xt@ .50em{\hss $\sim$\hss }\hfill \kern \z@
            }
            \makeatother
            \begin{document}
            """)
        # Two top squares to calibrate and identification band between them

        # Top left square.
        f.write(r"""
            \begin{{tikzpicture}}[scale={scale}]
            \draw[fill=black] (0,0) rectangle (1,1);
            \end{{tikzpicture}}""".format(scale=SQUARE_SIZE_IN_CM)
            )

        # Identification band
        n = identifier
        f.write(r"""\hfill
            \begin{{tikzpicture}}[scale={scale}]
            \draw[fill=black] (-1,0) rectangle (0,1);
            """.format(scale=SQUARE_SIZE_IN_CM)
            )

        for i in range(15):
            f.write(r"""\draw[fill={color}] ({x1},0) rectangle ({x2},1);
                """.format(color=("black" if n%2 else "white"), x1=i, x2=i+1))
            n = n//2

        f.write(r"""\draw (15, .5) node [right] {{\tiny{identifier}}};
            \end{{tikzpicture}}
            \hfill
            """.format(**locals())
            )

        # Top right square.
        f.write(r"""\begin{{tikzpicture}}[scale={scale}]
            \draw[fill=black] (0,0) rectangle (1,1);
            \end{{tikzpicture}}
            """.format(scale=SQUARE_SIZE_IN_CM)
            )

        # Header delimiter.

        f.write(r"""

            \vspace{-1em}
            \begin{scriptsize}\hfill\textsc{Ne rien écrire ci-dessus.}\hfill\hfill\hfill\textsc{Ne rien écrire ci-dessus.}\hfill\hfil\end{scriptsize}

            \simfill

            """)


        # Generate students list.
        try:
            f.write(r'''\begin{center}
                \begin{tikzpicture}[scale=.25]
                \draw [fill=black] (-2,0) rectangle (-1,1) (-1.5,0) node[below] {\tiny\rotatebox{-90}{\texttt{\textbf{Cochez le nom}}}};''')
            with open('liste_eleves.csv') as g:
                l = list(csv.reader(g))
                n_students = len(l)
                for i, row in enumerate(reversed(l)):
                    name = ' '.join(item.strip() for item in row)
                    if len(name) >= 15:
                        _name = name[:13].strip()
                        if " " not in name[12:13]:
                            _name += "."
                        name = _name
                    a = 2*i
                    b = a + 1
                    c = a + 0.5
                    color = ('black' if _n_student == n_students - i else 'white')
                    f.write(r'''\draw[fill={color}] ({a},0) rectangle ({b},1) ({c},0) node[below]
                        {{\tiny \rotatebox{{-90}}{{\texttt{{{name}}}}}}};'''.format(**locals()))
            b += 1
            f.write(r'''\draw[rounded corners] (-3,2) rectangle ({b}, -6.5);
                \draw[] (-0.5,2) -- (-0.5,-6.5);
                \end{{tikzpicture}}
                \end{{center}}'''.format(**locals()))
        except FileNotFoundError:
            print("Warning: liste_eleves.csv not found.")
            n_students = 0



        # Generate the table where students will answer.
        scale = CELL_SIZE_IN_CM
        f.write(r"""\hfill\hfill Réponses~:\hfill
            \begin{{tikzpicture}}[scale={scale}]
            \draw[fill=black] (-1,0) rectangle (0,1);
            """.format(**locals())
            )

        if isinstance(questions, int):
            questions = range(1, questions + 1)

        # Not all iterables have a .__len__() method, so calculate it.
        n_questions = 0

        for x1, name in enumerate(questions):
            x2=x1 + 1
            x3=.5*(x1 + x2)
            f.write(r"""\draw ({x1},0) rectangle ({x2},1) ({x3},0.5) node {{{name}}};
                """.format(**locals())
                )
            n_questions += 1

        if isinstance(answers, int):
            answers = ascii_letters[:answers]

        for i, name in enumerate(answers):
            y1 = -i
            y2 = y1 - 1
            y3 = .5*(y1 + y2)
            f.write(r"""
                \draw (-1,{y1}) rectangle (0,{y2}) (-0.5,{y3}) node {{{name}}};
                """.format(**locals())
                )
            for x1 in range(n_questions):
                opt = options.get((x1, i), "")
                x2=x1 + 1
                f.write(r"""\draw [{opt}] ({x1},{y1}) rectangle ({x2},{y2});
                    """.format(**locals())
                    )

        n_answers = i + 1

        f.write(r"""
\end{tikzpicture}
\hfill\hfill\hfil
""")



        # That's all folks !
        f.write(r"\end{document}")


    # Generate a config file:
    with open("%s.config" % filename, "w") as f:
        f.write("# n_questions is the number of questions.\n")
        f.write('n_questions = %s\n' % n_questions)
        f.write('# n_answers is the number of answers per question.\n')
        f.write('n_answers = %s\n' % n_answers)
        f.write('# Length of students list (0 if no list at all)\n')
        f.write('n_students = %s\n' % n_students)

