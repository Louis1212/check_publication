# check_publication

This side project is mainly to help my part-time job, checking
for a research group wether the members have new publications that
are not yet listed on their website.

To run the graphic interface, type

``$ python UI.py''

fillout at minimal the Last name, and First name of the author.
And a list needed to be update will be in the output first_name.txt.

The crawler send query request to adsabs.harvard.edu, and gathers
the publication informations that matches the author, parses them,
and output a list of reference in AGU style, in reverse chronological
order.

optionally, can provide a already existing list to check against,
in paper.txt, and abst.txt respectively for peer-reviewd paper
and published abstracts.

Note, the abstracts references are not yet in AGU style. Maybe
add this feature later.