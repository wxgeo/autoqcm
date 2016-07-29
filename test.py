from importlib import reload
from scriptlib import command
import generate
import scan

def test():
    reload(generate)
    reload(scan)
    id0 = 1173
    # 1173 = 1 + 4 + 16 + 128 + 1024 → ■■□■□■□□■□□■□□□□
    #
    #     ■   ■ □ ■ □ ■  □  □   ■   □   □   ■    □    □    □     □
    #   start 1 2 4 8 16 32 64 128 256 512 1024 2048 4096 8192 16384
    questions0 = ["A1","A2","B1","B2","C", "D"]
    n_answers0 = 5

    generate.generate_tex(filename="test", identifier=id0,
                 questions=questions0,
                 answers=n_answers0,
                           )
    command("pdflatex test.tex")
    command("inkscape -f test.pdf -b white -d 150 -e test.png")
    id1, answers = scan.scan_picture("test.png", "test.config")
    assert(id1 == id0)
    assert(len(questions0) == len(answers))
    assert(all(n_answers0 == len(answer) for answer in answers))

