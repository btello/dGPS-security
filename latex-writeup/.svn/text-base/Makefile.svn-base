PAPERNAME=01
TEXFILES =  *.tex

$(PAPERNAME).pdf : $(TEXFILES) $(PAPERNAME).tex biblio.bib
	pdflatex $(PAPERNAME)
	bibtex $(PAPERNAME)
	pdflatex $(PAPERNAME)
	pdflatex $(PAPERNAME)
clean:
	rm -f *.ps $(PAPERNAME).pdf *.dvi *.aux *.log *.blg *.bbl *~ *.ilg *.idx *.out *.in
