from importlib import reload
from numpy import array

from scriptlib import command
import generate
import scan

def test1():
    reload(generate)
    reload(scan)
    id0 = 1173
    # 1173 = 1 + 4 + 16 + 128 + 1024 → ■■□■□■□□■□□■□□□□
    #
    #     ■   ■ □ ■ □ ■  □  □   ■   □   □   ■    □    □    □     □
    #   start 1 2 4 8 16 32 64 128 256 512 1024 2048 4096 8192 16384
    questions0 = ["A1","A2","B1","B2","C", "D", "E1", "E2", "E3",
                    10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    n_answers0 = 5
    n_student0 = 27
    name = "test1"

    generate.generate_tex(filename=name, identifier=id0,
                 questions=questions0,
                 answers=n_answers0,
                 options={
                 (2, 3):"fill=blue!50!gray!50!white",
                 (4, 1): "fill=black",
                 (7, 2): "fill=red",
                 (19, 4):"fill=green!50!gray!50!white",
                 (19, 3):"fill=black!20!white",
                 },
                 #_n_student=n_student0,
                           )
    command("pdflatex %s.tex" % name)
    command("inkscape -f %s.pdf -b white -d 150 -e %s.png" % (name, name))
    id1, answers, n_student1 = scan.scan_picture("%s.png" % name, "%s.config" % name)
    assert id1 == id0
    #assert n_student1 == n_student0
    assert len(questions0) == len(answers)
    assert all(n_answers0 == len(answer) for answer in answers)
    assert (array(answers).nonzero() == array(([2, 4, 7, 19, 19], [3, 1, 2, 3, 4]))).all()
    return ((id1, answers, n_student1))

def test2():
    reload(generate)
    reload(scan)
    id0 = 27
    # 1173 = 1 + 4 + 16 + 128 + 1024 → ■■□■□■□□■□□■□□□□
    #
    #     ■   ■ □ ■ □ ■  □  □   ■   □   □   ■    □    □    □     □
    #   start 1 2 4 8 16 32 64 128 256 512 1024 2048 4096 8192 16384
    questions0 = 20
    n_answers0 = 8
    name = "test2"

    generate.generate_tex(filename=name, identifier=id0,
                 questions=questions0,
                 answers=n_answers0,
                 options={
                 (2, 3):"fill=blue!50!gray!50!white",
                 (4, 1): "fill=black",
                 (7, 2): "fill=red",
                 (19, 4):"fill=green!50!gray!50!white",
                 (19, 3):"fill=black!20!white",
                 },
                           )
    command("pdflatex %s.tex" % name)
    command("inkscape -f %s.pdf -b white -d 150 -e %s.png" % (name, name))
    id1, answers, n_student1 = scan.scan_picture("%s.png" % name, "%s.config" % name)
    assert id1 == id0
    assert n_student1 is None
    assert questions0 == len(answers)
    assert all(n_answers0 == len(answer) for answer in answers)
    assert (array(answers).nonzero() == array(([2, 4, 7, 19, 19], [3, 1, 2, 3, 4]))).all()
    return ((id1, answers, n_student1))



