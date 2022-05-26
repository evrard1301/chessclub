all:
	pdflatex -shell-escape slides.tex
	pdflatex -shell-escape slides.tex

clean:
	rm -f *.aux *.log *.nav *.out *.snm *.toc

mrproper: clean
	rm -f *.pdf
