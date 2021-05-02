clc;
clear;
[x,y,z] = meshgrid(-5:0.1:5);
c1 = -x-2*y+z+4;
c2 = -x+y-z-2;
c11 = c1<=0 & c2<=0;
fv2 = isosurface(x,y,z,c11,0);

figure
p1 = patch(fv2);
isonormals(x,y,z,c11,p1)
set(p1,'facecolor',[0 .5 1],'edgecolor','none')
view(150,30),axis image,grid on
camlight
lighting gouraud