import re,glob
pairs = {
 'synchronisation':'synchronization','synchronised':'synchronized','synchronise':'synchronize',
 'minimises':'minimizes','minimise':'minimize','minimised':'minimized',
 'recognising':'recognizing','Recognising':'Recognizing','recognise':'recognize','recognised':'recognized',
 'penalises':'penalizes','localisation':'localization','localised':'localized','Localisation':'Localization',
 'optimisation':'optimization','optimiser':'optimizer','optimised':'optimized','optimise':'optimize','optimises':'optimizes',
 'normalising':'normalizing','normalise':'normalize','normalised':'normalized',
 'summarises':'summarizes','summarised':'summarized','summarise':'summarize','Summarising':'Summarizing','summarising':'summarizing',
 'linearises':'linearizes','linearised':'linearized','linearise':'linearize','Linearise':'Linearize','linearisation':'linearization',
 'maximised':'maximized','maximise':'maximize','digitised':'digitized','digitise':'digitize',
 'reorganising':'reorganizing','organised':'organized','realise':'realize','standardise':'standardize','utilise':'utilize',
 'colour':'color','coloured':'colored','colours':'colors','Colour':'Color',
 'centre':'center','centred':'centered','centres':'centers','Centre':'Center',
 'neighbours':'neighbors','neighbour':'neighbor','Neighbours':'Neighbors',
 'kilometres':'kilometers','kilometre':'kilometer','centimetres':'centimeters','centimetre':'centimeter',
 'millimetres':'millimeters','millimetre':'millimeter','metres':'meters','metre':'meter',
 'travelled':'traveled','travelling':'traveling','labelled':'labeled','levelled':'leveled','unlevelled':'unleveled',
 'modelled':'modeled','modelling':'modeling','signalled':'signaled',
 'practised':'practiced','analogue':'analog','tyre':'tire','behaviour':'behavior','favour':'favor','grey':'gray',
 'favourite':'favorite','programme':'program','catalogue':'catalog','fibre':'fiber','licence':'license',
}
files = glob.glob('ch*.tex')+glob.glob('figs*.py')
for f in files:
    s=open(f).read(); o=s
    for a,b in pairs.items():
        s=re.sub(r'\b'+a+r'\b', b, s)
    if s!=o: open(f,'w').write(s); print('updated',f)
