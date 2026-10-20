// Execute the exact bundled GLTFLoader without a DOM, browser or WebGL context.
// This checks loader/extension compatibility and loaded scene identities/bounds;
// it is deliberately not presented as visual or interaction testing.
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import * as THREE from '../../inspector/vendor/three/build/three.module.js';
import { GLTFLoader } from '../../inspector/vendor/three/examples/jsm/loaders/GLTFLoader.js';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const manifest = JSON.parse(await fs.readFile(path.join(root, 'inspector/assets/cad-manifest.json'), 'utf8'));
if (!process.argv.includes('--partial')) assert.equal(manifest.models.length, 10, 'All ten inspection models must exist');
const results = [];
for (const model of manifest.models) {
  const bytes = await fs.readFile(path.join(root, 'inspector', model.file));
  const buffer = bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength);
  const loaded = await new GLTFLoader().parseAsync(buffer, '');
  const expected = new Set(model.parts.map((part) => part.id)), found = new Set();
  loaded.scene.traverse((object) => { if (object.userData.id != null && expected.has(String(object.userData.id))) found.add(String(object.userData.id)); });
  assert.deepEqual([...found].sort(), [...expected].sort(), model.id + ' part identity mismatch');
  const bounds = new THREE.Box3().setFromObject(loaded.scene, true);
  const actual = [bounds.min.toArray(), bounds.max.toArray()];
  let maxError = 0;
  for (let edge = 0; edge < 2; edge++) for (let axis = 0; axis < 3; axis++) {
    assert(Number.isFinite(actual[edge][axis]));
    maxError = Math.max(maxError, Math.abs(actual[edge][axis] - model.bounds[edge][axis]));
  }
  assert(maxError <= .0003, `${model.id}: loaded metre/Y-up bounds differ by ${maxError}`);
  results.push({ id: model.id, loadedParts: found.size, maximumBoundErrorMM: maxError * 1000 });
  loaded.scene.traverse((object) => { object.geometry?.dispose(); for (const material of [object.material || []].flat()) material.dispose(); });
}
console.log(JSON.stringify({ passed: true, scope: 'Actual bundled Three.js GLTFLoader without browser/WebGL', models: results }));
