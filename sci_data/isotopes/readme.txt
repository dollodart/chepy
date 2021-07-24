One observation is that the isotope entropy is higher on average for orbital
numbers which are even, regardless of the orbital type (s, p, d, or f). Since
even numbers mean the outermost orbital has a spin pair, perhaps there is
something about having a spin pair that makes the nuclueus more stable for
larger number of isotopes--but it is unlikely the electron shells would affect
the nuclear stability (there is an entire separate nuclear strong force from
the electrostatic interactions of electrons and protons).

Because the number of oribtals filled in a type (s, p, d, f) is
necessarily even, since even when orbital types are odd numbers (like 3
for px, py, pz) it is multiplied by 2 for the up and down spin state,
this trend is also captured in the parity of the group number.

Data source: The isotope data was taken from a NIST website. There were difficulties
with the encoding. I had to first copy-paste in a windows environment to an Excel
sheet. Then export to csv, and on linux do 

cat orig.csv | iconv -f utf-8 -t ascii//translit > alt.csv

to change the text encoding so that the escape characters representing spaces
can be found and deleted by Vim. Using python's .readlines() method and repr()
function also the characters to be seen (\xa, \xa0).

See also ase.data.isotopes for the same thing obtained through an API.
Pubchempy lets you query directly from python for isotope data as is shown in
the script in this directory.
