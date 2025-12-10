import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { OBJLoader } from 'three/addons/loaders/OBJLoader.js';
import { STLLoader } from 'three/addons/loaders/STLLoader.js';
import GUI from 'lil-gui';
import { LogSpiral } from './LogSpiral.js';

class App {
  constructor() {
    this.params = {
      // Spiral parameters
      a: 3.5,
      k: 0.7,
      radiusScale: 1,
      heightScale: 10,
      lowerBound: 100,
      truncatePercentage: 0.4,
      
      // Viewing parameters
      speed: 1,
      objectScale: 2,
      
      // Toggles
      animating: false,
      showCurve: true,
      showModel: true,
      
      // Model selection
      modelChoice: 'bunny',
      
      // Actions
      loadModel: () => this.openModelDialog(),
      reset: () => this.reset()
    };

    this.modelOptions = ['chicken', 'bunny', 'snowman', 'diamond'];
    
    // Base model size before scale multiplier is applied
    this.baseModelSize = 100;

    this.curve = [];
    this.progress = 0;
    this.clock = new THREE.Clock();
    this.frameCount = 0;
    this.lastFpsUpdate = 0;

    this.init();
    this.setupLighting();
    this.setupGUI();
    this.setupKeyboardControls();
    this.createSpiral();
    this.loadDefaultModel();
    this.animate();
  }

  init() {
    // Scene
    this.scene = new THREE.Scene();
    this.scene.background = new THREE.Color(0x00008a);

    // Camera
    this.camera = new THREE.PerspectiveCamera(
      60,
      window.innerWidth / window.innerHeight,
      0.1,
      50000
    );
    this.camera.position.set(500, 300, 500);

    // Renderer
    const canvas = document.getElementById('canvas');
    this.renderer = new THREE.WebGLRenderer({
      canvas,
      antialias: true,
      alpha: true
    });
    this.renderer.setSize(window.innerWidth, window.innerHeight);
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    this.renderer.shadowMap.enabled = true;
    this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    this.renderer.toneMapping = THREE.ACESFilmicToneMapping;
    this.renderer.toneMappingExposure = 1.2;

    // Controls (for non-animated viewing)
    this.controls = new OrbitControls(this.camera, this.renderer.domElement);
    this.controls.enableDamping = true;
    this.controls.dampingFactor = 0.05;
    this.controls.target.set(0, 0, 0);

    // Ground plane with grid
    this.createGround();

    // Handle resize
    window.addEventListener('resize', () => this.onResize());
  }

  createGround() {
    // Grid helper - black wireframes
    const gridHelper = new THREE.GridHelper(2000, 50, 0xffffff, 0xffffff);
    gridHelper.material.opacity = 0.25;
    gridHelper.material.transparent = true;
    this.scene.add(gridHelper);

    // Axes helper (RGB = XYZ) - raised slightly to prevent z-fighting with grid
    const axesHelper = new THREE.AxesHelper(500);
    axesHelper.position.y = 1;
    this.scene.add(axesHelper);
  }

  setupLighting() {
    // Ambient light
    const ambientLight = new THREE.AmbientLight(0x404060, 0.5);
    this.scene.add(ambientLight);

    // Main directional light
    const directionalLight = new THREE.DirectionalLight(0xffffff, 1.2);
    directionalLight.position.set(100, 200, 100);
    directionalLight.castShadow = true;
    directionalLight.shadow.mapSize.width = 2048;
    directionalLight.shadow.mapSize.height = 2048;
    directionalLight.shadow.camera.near = 0.5;
    directionalLight.shadow.camera.far = 1000;
    directionalLight.shadow.camera.left = -200;
    directionalLight.shadow.camera.right = 200;
    directionalLight.shadow.camera.top = 200;
    directionalLight.shadow.camera.bottom = -200;
    this.scene.add(directionalLight);

    // Accent lights for atmosphere
    const cyanLight = new THREE.PointLight(0x00f0ff, 0.8, 500);
    cyanLight.position.set(-100, 50, 100);
    this.scene.add(cyanLight);

    const magentaLight = new THREE.PointLight(0xff00aa, 0.5, 400);
    magentaLight.position.set(100, 80, -100);
    this.scene.add(magentaLight);

    // Hemisphere light for natural feel
    const hemiLight = new THREE.HemisphereLight(0x0088ff, 0x002244, 0.4);
    this.scene.add(hemiLight);
  }

  setupGUI() {
    this.gui = new GUI({ title: '⟨ SPIRAL CONTROLS ⟩' });
    
    // Position GUI at bottom left
    this.gui.domElement.style.position = 'absolute';
    this.gui.domElement.style.bottom = '20px';
    this.gui.domElement.style.left = '20px';
    this.gui.domElement.style.top = 'auto';
    this.gui.domElement.style.right = 'auto';

    // Spiral folder
    const spiralFolder = this.gui.addFolder('Spiral Parameters');
    spiralFolder.add(this.params, 'a', 0, 10, 0.01).name('a coefficient').onChange(() => this.createSpiral());
    spiralFolder.add(this.params, 'k', 0.01, 1, 0.01).name('k coefficient').onChange(() => this.createSpiral());
    spiralFolder.add(this.params, 'radiusScale', 0.1, 10, 0.1).name('Radius Scale').onChange(() => this.createSpiral());
    spiralFolder.add(this.params, 'heightScale', 1, 12, 0.1).name('Height Scale').onChange(() => this.createSpiral());
    spiralFolder.add(this.params, 'lowerBound', -100, 100, 1).name('Lift').onChange(() => this.createSpiral());
    spiralFolder.add(this.params, 'truncatePercentage', 0.001, 1, 0.01).name('Truncate').onChange(() => this.createSpiral());
    spiralFolder.open();

    // View folder
    const viewFolder = this.gui.addFolder('Viewing');
    viewFolder.add(this.params, 'speed', 0.01, 3, 0.01).name('Animation Speed');
    viewFolder.add(this.params, 'objectScale', 0.1, 10, 0.1).name('Model Scale').onChange(() => this.updateModelScale());
    viewFolder.open();

    // Toggles folder
    const togglesFolder = this.gui.addFolder('Toggles');
    togglesFolder.add(this.params, 'animating').name('Animate (G)');
    togglesFolder.add(this.params, 'showCurve').name('Show Curve (C)').onChange(() => this.toggleCurveVisibility());
    togglesFolder.add(this.params, 'showModel').name('Show Model (H)').onChange(() => this.toggleModelVisibility());
    togglesFolder.open();

    // Model folder
    const modelFolder = this.gui.addFolder('Model');
    modelFolder.add(this.params, 'modelChoice', this.modelOptions).name('Default Model').onChange(() => this.loadSelectedModel());
    modelFolder.add(this.params, 'loadModel').name('📁 Load Custom...');
    modelFolder.open();

    // Actions folder
    const actionsFolder = this.gui.addFolder('Actions');
    actionsFolder.add(this.params, 'reset').name('🔄 Reset');
  }

  setupKeyboardControls() {
    window.addEventListener('keydown', (e) => {
      switch(e.key.toLowerCase()) {
        case 'escape':
          // Could close GUI or similar
          break;
        case 'r':
          this.reset();
          break;
        case 'g':
          this.params.animating = !this.params.animating;
          this.gui.controllers.forEach(c => c.updateDisplay());
          break;
        case 'c':
          this.params.showCurve = !this.params.showCurve;
          this.toggleCurveVisibility();
          this.gui.controllers.forEach(c => c.updateDisplay());
          break;
        case 'h':
          this.params.showModel = !this.params.showModel;
          this.toggleModelVisibility();
          this.gui.controllers.forEach(c => c.updateDisplay());
          break;
      }
    });
  }

  createSpiral() {
    // Remove old spiral
    if (this.spiralLine) {
      this.scene.remove(this.spiralLine);
      this.spiralLine.geometry.dispose();
      this.spiralLine.material.dispose();
    }

    // Generate new spiral using LogSpiral class
    const spiral = new LogSpiral(this.params);
    this.curve = spiral.generateCurve();
    

    // Create line geometry
    const points = this.curve.map(p => new THREE.Vector3(p.x, p.z, p.y)); // Swap Y/Z for Three.js coord system
    const geometry = new THREE.BufferGeometry().setFromPoints(points);

    const material = new THREE.LineBasicMaterial({
      color: 0xff0000,
      linewidth: 2
    });

    this.spiralLine = new THREE.Line(geometry, material);
    this.spiralLine.visible = this.params.showCurve;
    this.scene.add(this.spiralLine);

    // Reset progress
    this.progress = 0;
  }

  loadDefaultModel() {
    this.loadSelectedModel();
  }

  loadSelectedModel() {
    // Remove old model
    if (this.viewingObject) {
      this.scene.remove(this.viewingObject);
      this.viewingObject.traverse((child) => {
        if (child.geometry) child.geometry.dispose();
        if (child.material) child.material.dispose();
      });
    }

    const material = new THREE.MeshBasicMaterial({
      color: 0xffffff,
      wireframe: true,
      transparent: true,
      opacity: 0.6
    });

    const modelPath = `${import.meta.env.BASE_URL}models/${this.params.modelChoice}.obj`;
    const loader = new OBJLoader();
    
    console.log(`Loading model from: ${modelPath}`);
    
    loader.load(
      modelPath,
      (obj) => {
        console.log('Model loaded successfully:', obj);
        
        let meshCount = 0;
        let vertexCount = 0;
        
        obj.traverse((child) => {
          if (child instanceof THREE.Mesh) {
            meshCount++;
            if (child.geometry) {
              vertexCount += child.geometry.attributes.position?.count || 0;
              // Ensure geometry is valid
              if (!child.geometry.attributes.position || child.geometry.attributes.position.count === 0) {
                console.warn('Mesh has no vertices:', child);
              }
            }
            child.material = material;
          }
        });
        
        console.log(`Model contains ${meshCount} meshes with ${vertexCount} total vertices`);
        
        if (meshCount === 0) {
          console.error('Model loaded but contains no meshes!');
          // Fallback to icosahedron
          const geometry = new THREE.IcosahedronGeometry(25, 2);
          this.viewingObject = new THREE.Mesh(geometry, material);
          this.viewingObject.userData.baseScale = this.baseModelSize;
          this.viewingObject.scale.setScalar(this.baseModelSize * this.params.objectScale);
          this.viewingObject.visible = this.params.showModel;
          this.scene.add(this.viewingObject);
          return;
        }
        
        this.viewingObject = obj;
        this.viewingObject.userData.baseScale = this.baseModelSize;
        this.viewingObject.scale.setScalar(this.baseModelSize * this.params.objectScale);
        this.centerModel(this.viewingObject);
        this.viewingObject.visible = this.params.showModel;
        this.scene.add(this.viewingObject);
        
        // Log bounding box for debugging
        const box = new THREE.Box3().setFromObject(this.viewingObject);
        console.log('Model bounding box:', box);
        console.log('Model position:', this.viewingObject.position);
        console.log('Model scale:', this.viewingObject.scale);
        console.log('Model visible:', this.viewingObject.visible);
      },
      (progress) => {
        if (progress.lengthComputable) {
          const percentComplete = (progress.loaded / progress.total) * 100;
          console.log(`Model loading: ${percentComplete.toFixed(2)}%`);
        }
      },
      (error) => {
        console.error(`Failed to load ${this.params.modelChoice} model:`, error);
        // Fallback to icosahedron if model fails to load
        const geometry = new THREE.IcosahedronGeometry(25, 2);
        this.viewingObject = new THREE.Mesh(geometry, material);
        this.viewingObject.userData.baseScale = this.baseModelSize;
        this.viewingObject.scale.setScalar(this.baseModelSize * this.params.objectScale);
        this.viewingObject.visible = this.params.showModel;
        this.scene.add(this.viewingObject);
      }
    );
  }

  openModelDialog() {
    const input = document.getElementById('model-input');
    input.click();
    
    input.onchange = (e) => {
      const file = e.target.files[0];
      if (file) {
        this.loadModelFile(file);
      }
    };
  }

  loadModelFile(file) {
    const extension = file.name.split('.').pop().toLowerCase();
    const url = URL.createObjectURL(file);

    // Remove old model
    if (this.viewingObject) {
      this.scene.remove(this.viewingObject);
      if (this.viewingObject.geometry) this.viewingObject.geometry.dispose();
      if (this.viewingObject.material) this.viewingObject.material.dispose();
    }

    const material = new THREE.MeshBasicMaterial({
      color: 0xffffff,
      wireframe: true,
      transparent: true,
      opacity: 0.1
    });

    if (extension === 'obj') {
      const loader = new OBJLoader();
      loader.load(url, (obj) => {
        obj.traverse((child) => {
          if (child instanceof THREE.Mesh) {
            child.material = material;
          }
        });
        this.viewingObject = obj;
        this.viewingObject.userData.baseScale = this.baseModelSize;
        this.viewingObject.scale.setScalar(this.baseModelSize * this.params.objectScale);
        this.centerModel(this.viewingObject);
        this.viewingObject.visible = this.params.showModel;
        this.scene.add(this.viewingObject);
        URL.revokeObjectURL(url);
      });
    } else if (extension === 'stl') {
      const loader = new STLLoader();
      loader.load(url, (geometry) => {
        geometry.computeVertexNormals();
        const mesh = new THREE.Mesh(geometry, material);
        this.viewingObject = mesh;
        this.viewingObject.userData.baseScale = this.baseModelSize;
        this.viewingObject.scale.setScalar(this.baseModelSize * this.params.objectScale);
        this.centerModel(this.viewingObject);
        this.viewingObject.visible = this.params.showModel;
        this.scene.add(this.viewingObject);
        URL.revokeObjectURL(url);
      });
    }
  }

  centerModel(model) {
    const box = new THREE.Box3().setFromObject(model);
    const center = box.getCenter(new THREE.Vector3());
    model.position.sub(center);
    model.position.y = 0; // Place on ground
  }

  updateModelScale() {
    if (this.viewingObject) {
      const baseScale = this.viewingObject.userData.baseScale || this.baseModelSize;
      this.viewingObject.scale.setScalar(baseScale * this.params.objectScale);
    }
  }

  toggleCurveVisibility() {
    if (this.spiralLine) {
      this.spiralLine.visible = this.params.showCurve;
    }
  }

  toggleModelVisibility() {
    if (this.viewingObject) {
      this.viewingObject.visible = this.params.showModel;
    }
  }

  reset() {
    this.params.a = 3.5;
    this.params.k = 0.7;
    this.params.radiusScale = 1;
    this.params.heightScale = 10;
    this.params.lowerBound = 100;
    this.params.truncatePercentage = 0.4;
    this.params.speed = 1;
    this.params.objectScale = 2;
    this.params.animating = false;
    this.params.showCurve = true;
    this.params.showModel = true;
    this.progress = 0;

    // Update GUI
    this.gui.controllersRecursive().forEach(c => c.updateDisplay());

    // Recreate spiral
    this.createSpiral();
    this.toggleCurveVisibility();
    this.toggleModelVisibility();
  }

  updateCamera(dt) {
    if (this.params.animating && this.curve.length > 0) {
      // Animate along curve
      this.progress += (dt / 10) * this.params.speed;
      if (this.progress > 1) this.progress = 0;

      const index = Math.floor(this.curve.length * this.progress);
      const point = this.curve[Math.min(index, this.curve.length - 1)];
      
      // Convert to Three.js coordinate system (swap Y and Z)
      this.camera.position.set(point.x, Math.max(point.z, 5), point.y);
      
      // Disable orbit controls during animation
      this.controls.enabled = false;
    } else {
      // Static viewing - orbit controls handle the camera
      this.controls.enabled = true;
    }

    // Always look at the viewing object
    if (this.viewingObject && this.params.animating) {
      this.camera.lookAt(this.viewingObject.position);
    }
  }

  updateFPS(time) {
    // FPS tracking (display removed)
    this.frameCount++;
    if (time - this.lastFpsUpdate >= 1000) {
      this.frameCount = 0;
      this.lastFpsUpdate = time;
    }
  }

  onResize() {
    const width = window.innerWidth;
    const height = window.innerHeight;

    this.camera.aspect = width / height;
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(width, height);
  }

  animate() {
    requestAnimationFrame((time) => {
      this.animate();
      this.updateFPS(time);
    });

    const dt = this.clock.getDelta();

    this.updateCamera(dt);
    this.controls.update();
    this.renderer.render(this.scene, this.camera);
  }
}

// Start the application
new App();

