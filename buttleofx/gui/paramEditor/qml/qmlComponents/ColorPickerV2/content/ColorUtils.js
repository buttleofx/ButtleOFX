// creates color value from hue, saturation, valueOf(), alpha
function hsva2QtHsla(h, s, v, a) {
    var lightness = (2 - s)*v;
    var satHSL = s*v/((lightness <= 1) ? lightness : 2 - lightness);
    lightness /= 2;
    return Qt.hsla(h, satHSL, lightness, a);
}

// CONVERT RGB(A) -> HSV(A)

function hsv2rgb(hsv)
{
    var h = hsv.x, s = hsv.y, v = hsv.z ;

    var r, g, b, i, f, p, q, t;
    i = Math.floor(h * 6);
    f = h * 6 - i;
    p = v * (1 - s);
    q = v * (1 - f * s);
    t = v * (1 - (1 - f) * s);
    switch (i % 6) {
        case 0: r = v; g = t; b = p; break;
        case 1: r = q; g = v; b = p; break;
        case 2: r = p; g = v; b = t; break;
        case 3: r = p; g = q; b = v; break;
        case 4: r = t; g = p; b = v; break;
        case 5: r = v; g = p; b = q; break;
    }

    return Qt.vector3d(r, g, b);
}

function hsva2rgba(hsva) {
    var rgb = hsv2rgb(Qt.vector3d(hsva.x, hsva.y, hsva.z))
    return Qt.vector4d(rgb.x, rgb.y, rgb.z, hsva.w);
}

// CONVERT RGB(A) -> HSV(A)

function rgb2hsv(rgb)
{
    var r = rgb.x;
    var g = rgb.y;
    var b = rgb.z;
    var max = Math.max(r, g, b), min = Math.min(r, g, b);
    var h, s, v = max;

    var d = max - min;
    s = max === 0 ? 0 : d / max;

    if(max == min){
        h = 0; // achromatic
    } else{
        switch(max){
            case r:
                h = (g - b) / d + (g < b ? 6 : 0);
                break;
            case g:
                h = (b - r) / d + 2;
                break;
            case b:
                h = (r - g) / d + 4;
                break;
        }
        h /= 6;
    }


    return Qt.vector3d(h, s, v);
}

function rgba2hsva(rgba)
{
    var hsv = rgb2hsv(Qt.vector3d(rgba.x, rgba.y, rgba.z))
    return Qt.vector4d(hsv.x, hsv.y, hsv.z, rgba.w);
}

// HEXA TOOLS
// extracts integer color channel value [0..255] from color value
function getChannelStr(clr, channelIdx) {
    return parseInt(clr.toString().substr(channelIdx*2 + 1, 2), 16);
}

//convert to hexa with nb char
function intToHexa(val , nb)
{
    var hexaTmp = val.toString(16) ;
    var hexa = "";
    var size = hexaTmp.length
    if (size < nb )
    {
        for(var i = 0 ; i < nb - size ; ++i)
        {
            hexa += "0"
        }
    }
    return hexa + hexaTmp
}

function hexaFromRGBA(red, green, blue, alpha)
{
    return intToHexa(Math.round(red * 255), 2)+intToHexa(Math.round(green * 255), 2)+intToHexa(Math.round(blue * 255), 2);
}
