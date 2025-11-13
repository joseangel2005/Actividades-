/*
 * Script to draw a complex shape in 2D
 *
 * Gilberto Echeverria
 * Jose Angel De La Cruz Alonso/ A01772695
 * 2025-07-12
 */


'use strict';

import * as twgl from 'twgl-base.js';
import { square, bigote } from '../libs/shapes.js';
import { M3 } from '../libs/2d-lib.js';
import GUI from 'lil-gui';

// Define the shader code, using GLSL 3.00
const vsGLSL = `#version 300 es
in vec2 a_position;
in vec4 a_color;

uniform vec2 u_resolution;
uniform mat3 u_transforms;

out vec4 v_color;

void main() {
    vec2 position = (u_transforms * vec3(a_position, 1)).xy;
    vec2 zeroToOne = position / u_resolution;
    vec2 zeroToTwo = zeroToOne * 2.0;
    vec2 clipSpace = zeroToTwo - 1.0;
    gl_Position = vec4(clipSpace * vec2(1, -1), 0, 1);
    v_color = a_color;
}
`;

const fsGLSL = `#version 300 es
precision highp float;

in vec4 v_color;
out vec4 outColor;

void main() {
    outColor = v_color;
}
`;

// Estructura para los datos globales de todos los objetos
const objects = {
    model: {
        transforms: {
            t: {
                x: 280,
                y: 265,
                z: 0,
            },
            rr: {
                x: 0,
                y: 0,
                z: 0,
            },
            s: {
                x: 1,
                y: 1,
                z: 1,
            }
        },
        color: [219, 169, 140, 255] 
    },
    pivot: {
        transforms: {
            t: {
                x: 280,
                y: 280,
                z: 0,
            },
        },
    }
}

// Initialize the WebGL environment
function main() {
    const canvas = document.querySelector('canvas');
    const gl = canvas.getContext('webgl2');
    twgl.resizeCanvasToDisplaySize(gl.canvas);
    gl.viewport(0, 0, gl.canvas.width, gl.canvas.height);

    setupUI(gl);

    const programInfo = twgl.createProgramInfo(gl, [vsGLSL, fsGLSL]); 

    // Crear buffers para la cara
    const arrays = square(50);
    const bufferInfo = twgl.createBufferInfoFromArrays(gl, arrays);
    const vao = twgl.createVAOFromBufferInfo(gl, programInfo, bufferInfo);

    // Crear buffers para el bigote (Pivot)
    const arraysPivot = bigote(50);
    const bufferInfoPivot = twgl.createBufferInfoFromArrays(gl, arraysPivot);
    const vaoPivot = twgl.createVAOFromBufferInfo(gl, programInfo, bufferInfoPivot);

    drawScene(gl, vao, programInfo, bufferInfo, vaoPivot, bufferInfoPivot);
}

// Function to do the actual display of the objects
function drawScene(gl, vao, programInfo, bufferInfo, vaoPivot, bufferInfoPivot) {
    gl.clearColor(1, 1, 1, 1);
    gl.clear(gl.COLOR_BUFFER_BIT);

    gl.useProgram(programInfo.program);

    // Obtener las transformaciones de la cara para enviarlas al shader y dibujar la cara
    let translate = [objects.model.transforms.t.x, objects.model.transforms.t.y];
    
    // se agrega esta linea para obtener la posicion del pivote para despues usarla en las transformaciones
    let pivotPoint = [objects.pivot.transforms.t.x, objects.pivot.transforms.t.y];
    
    // en las dos lineas de abajo lo queharemos: obtener el angulo de rotacion y la escala para despues usarlas en las transformaciones
    let angle_radians = objects.model.transforms.rr.z; // aqui en especifico solo rotacion en z
    let scale = [objects.model.transforms.s.x, objects.model.transforms.s.y];// luego aqui la escala en x y en  y

 // De aqui 

  //Basicamentew lo que haremos de la parte de donde de "De aqui" a "Aca" lo que heremos basicamente es modificar la
  // forma en que se hacen las transformaciones para que se hagan en base al pivote.
    
    let transforms = M3.identity(); // primero diremos que transforms es una matriz identidad en donde empezaremos a multiplicar las demas transformaciones
    
    transforms = M3.multiply(M3.scale(scale), transforms); // luego en transforms multiplicamos la matriz de escala por la matriz identidad
    
    let relativePos = [translate[0] - pivotPoint[0], translate[1] - pivotPoint[1]];// despues obtenemos la posicion relativa restando la posicion de la cara menos la posicion del pivote
    
    transforms = M3.multiply(M3.translation(relativePos), transforms);// aqui en transforms multiplicamos la matriz de traslacion recordando que  la traslacion es la posicion relativa que obtuvimos en la linea anterior

    transforms = M3.multiply(M3.rotation(angle_radians), transforms);// luego multiplamos transforms por la matriz de rotacion
    
    transforms = M3.multiply(M3.translation(pivotPoint), transforms); // luego multiplicamos transforms por la matriz de traslacion del pivote para regresar la figura a su posicion original
    
// Aca 

    let uniforms = {
        u_resolution: [gl.canvas.width, gl.canvas.height],
        u_transforms: transforms,
    }

    twgl.setUniforms(programInfo, uniforms);
    gl.bindVertexArray(vao);
    twgl.drawBufferInfo(gl, bufferInfo);

    // Dibujar el bigote 
    let translatePivot = [objects.pivot.transforms.t.x, objects.pivot.transforms.t.y];
    const traMatPivot = M3.translation(translatePivot);

    uniforms.u_transforms = traMatPivot;

    twgl.setUniforms(programInfo, uniforms);
    gl.bindVertexArray(vaoPivot);
    twgl.drawBufferInfo(gl, bufferInfoPivot);

    requestAnimationFrame(() => drawScene(gl, vao, programInfo, bufferInfo, vaoPivot, bufferInfoPivot));
}

function setupUI(gl) {
    const gui = new GUI();

    // Controles para la cara
    const modelFolder = gui.addFolder('Model');
    
    const traFolder = modelFolder.addFolder('Translation');
    traFolder.add(objects.model.transforms.t, 'x', 5, gl.canvas.width);
    traFolder.add(objects.model.transforms.t, 'y', 0, gl.canvas.height);

    const rotFolder = modelFolder.addFolder('Rotation');
    rotFolder.add(objects.model.transforms.rr, 'z', 0, Math.PI * 2);

    const scaFolder = modelFolder.addFolder('Scale');
    scaFolder.add(objects.model.transforms.s, 'x', -5, 5);
    scaFolder.add(objects.model.transforms.s, 'y', -5, 5);

    gui.addColor(objects.model, 'color');
    
    // Controles para el bigote (Pivot)
    const pivotFolder = gui.addFolder('Pivot');
    
    const traFolderPivot = pivotFolder.addFolder('Translation');
    traFolderPivot.add(objects.pivot.transforms.t, 'x', 5, gl.canvas.width);
    traFolderPivot.add(objects.pivot.transforms.t, 'y', 0, gl.canvas.height);
}

main()