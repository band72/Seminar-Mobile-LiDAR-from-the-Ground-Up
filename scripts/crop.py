from PIL import Image, ImageChops; import glob
for f in glob.glob('figs/*.png'):
  if 'cover' in f: continue
  im=Image.open(f).convert('RGB'); bg=Image.new('RGB',im.size,(255,255,255))
  bb=ImageChops.difference(im,bg).point(lambda p:255 if p>12 else 0).getbbox()
  if bb:
    m=12; bb=(max(bb[0]-m,0),max(bb[1]-m,0),min(bb[2]+m,im.width),min(bb[3]+m,im.height))
    if (bb[2]-bb[0])*(bb[3]-bb[1]) < 0.97*im.width*im.height: im.crop(bb).save(f)
