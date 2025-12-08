/**
 * LogSpiral - Generates a 3D logarithmic spiral curve
 * 
 * The logarithmic spiral (also known as equiangular spiral or growth spiral)
 * is defined by the polar equation: r = a * e^(k*θ)
 * 
 * Where:
 * - a: determines the initial radius (scale factor)
 * - k: determines the growth rate (how tightly wound the spiral is)
 * - θ (theta): the angle in radians
 * 
 * The 3D version adds a height component using the natural logarithm.
 */
export class LogSpiral {
  constructor(params) {
    this.a = params.a ?? 2;
    this.k = params.k ?? 0.5;
    this.radiusScale = params.radiusScale ?? 1;
    this.heightScale = params.heightScale ?? 5;
    this.lowerBound = params.lowerBound ?? 1;
    this.truncatePercentage = params.truncatePercentage ?? 0;
    
    // Curve generation parameters
    this.iterationCount = 10001;
    this.stepDelta = 0.001;
  }

  /**
   * Generate the spiral curve as an array of 3D points
   * @returns {Array<{x: number, y: number, z: number}>}
   */
  generateCurve() {
    const curve = [];
    const curveLength = this.stepDelta * this.iterationCount;
    const startIndex = 1 + (curveLength * this.truncatePercentage);

    for (let index = startIndex; index < curveLength; index += this.stepDelta) {
      const point = this.calculatePoint(index);
      curve.push(point);
    }

    // Reverse to start from the outer edge (matches original behavior)
    curve.reverse();
    
    return curve;
  }

  /**
   * Calculate a single point on the spiral
   * @param {number} theta - The angle parameter
   * @returns {{x: number, y: number, z: number}}
   */
  calculatePoint(theta) {
    // Logarithmic spiral equations:
    // r = a * e^(k*θ)
    // x = r * cos(θ)
    // y = r * sin(θ)
    // z = height_scale² * ln(θ) + lower_bound
    
    const radius = this.radiusScale * this.a * Math.pow(Math.E, this.k * theta);
    
    const x = radius * Math.cos(theta);
    const y = radius * Math.sin(theta);
    const z = (this.heightScale * this.heightScale) * Math.log(theta) + this.lowerBound;

    return { x, y, z };
  }

  /**
   * Get a point on the curve at a normalized position (0-1)
   * @param {Array} curve - The generated curve array
   * @param {number} t - Normalized position (0 to 1)
   * @returns {{x: number, y: number, z: number}}
   */
  static getPointAtProgress(curve, t) {
    const index = Math.floor(curve.length * Math.max(0, Math.min(1, t)));
    return curve[Math.min(index, curve.length - 1)];
  }

  /**
   * Interpolate between two points on the curve
   * @param {Array} curve - The generated curve array
   * @param {number} t - Normalized position (0 to 1)
   * @returns {{x: number, y: number, z: number}}
   */
  static interpolatePointAtProgress(curve, t) {
    const pos = t * (curve.length - 1);
    const index = Math.floor(pos);
    const frac = pos - index;

    if (index >= curve.length - 1) {
      return curve[curve.length - 1];
    }

    const p1 = curve[index];
    const p2 = curve[index + 1];

    return {
      x: p1.x + (p2.x - p1.x) * frac,
      y: p1.y + (p2.y - p1.y) * frac,
      z: p1.z + (p2.z - p1.z) * frac
    };
  }

  /**
   * Create a spiral with preset configurations
   */
  static presets = {
    // Tight spiral that rises quickly
    tight: {
      a: 0.5,
      k: 0.2,
      radiusScale: 1,
      heightScale: 2,
      lowerBound: 5,
      truncatePercentage: 0.1
    },
    // Wide, gentle spiral
    wide: {
      a: 1.0,
      k: 0.8,
      radiusScale: 2,
      heightScale: 0.5,
      lowerBound: 1,
      truncatePercentage: 0.3
    },
    // Golden ratio spiral approximation
    golden: {
      a: 1.0,
      k: 0.306, // ln(φ) / (π/2) ≈ 0.306
      radiusScale: 1,
      heightScale: 1,
      lowerBound: 0,
      truncatePercentage: 0.2
    },
    // Nautilus shell-like spiral
    nautilus: {
      a: 0.8,
      k: 0.17,
      radiusScale: 1.5,
      heightScale: 0.3,
      lowerBound: 2,
      truncatePercentage: 0.15
    }
  };

  /**
   * Get information about the current spiral configuration
   */
  getInfo() {
    const curveLength = this.stepDelta * this.iterationCount;
    const effectiveLength = curveLength * (1 - this.truncatePercentage);
    
    return {
      formula: `r = ${this.a} × e^(${this.k}θ)`,
      parameters: {
        a: this.a,
        k: this.k,
        radiusScale: this.radiusScale,
        heightScale: this.heightScale,
        lowerBound: this.lowerBound,
        truncatePercentage: this.truncatePercentage
      },
      curveInfo: {
        totalPoints: Math.floor(effectiveLength / this.stepDelta),
        thetaRange: [1 + (curveLength * this.truncatePercentage), curveLength],
        stepSize: this.stepDelta
      }
    };
  }
}

