.pragma library
Qt.include("mathUtils.js")

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

//convert to hexa with nb char min
function int2hexa(val , nb)
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

function rgb2hexa(rgb)
{
    return int2hexa(Math.round(rgb.x * 255), 2)+int2hexa(Math.round(rgb.y * 255), 2)+int2hexa(Math.round(rgb.z * 255), 2);
}

function rgba2hexa(rgba)
{
    return rgb2hexa(rgba)+int2hexa(Math.round(rgba.w * 255), 2);
}

function hexa2rgb(hexa)
{
   var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hexa)
   return Qt.vector3d(parseInt(result[1], 16)/255, parseInt(result[2], 16)/255,parseInt(result[3], 16)/255)
}

// COMPLEMENTARY COLORS

// hsv is a vec3 with 0-1 value complementary color base on RGB Model
function complementaryColorHSVA(hsva) {
    var hue = hsv.x + 0.5
    if (hue > 1 )
        hue--

    return Qt.vector4d(hue, hsva.y, hsva.z, hsva.w)
}

// rgb is a vec3 with 0-1 value complementary color base on RGB Model
function complementaryColorRGBA(rgba){
    return Qt.vector4d(1 - rgba.x, 1 - rgba.y, 1 - rgba.z, rgba.w)
}

// OTHERS
function isGreyLvlColor(rgba)
{
    return rgba.x === rgba.y && rgba.y === rgba.z
}

function roundColor4D(color4D, precision) {
    color4D.x = decimalRound(color4D.x, precision)
    color4D.y = decimalRound(color4D.y, precision)
    color4D.z = decimalRound(color4D.z, precision)
    color4D.w = decimalRound(color4D.w, precision)
    return color4D
}
