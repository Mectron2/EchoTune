#version 330 core
uniform sampler2D image;
uniform float texOffsetX;
uniform float texOffsetY;
uniform int radius;
uniform float bloomIntensity; // Control the intensity of the bloom effect
uniform float stretchFactorX; // Additional factor to control the stretch on the X-axis

out vec4 color;
in vec2 fragmentTexCoord;

void main() {
    vec4 bloom = vec4(0.0);
    float totalWeight = 0.0;
    vec2 coord;

    // Calculate the bloom effect with stretched X-axis
    for(int y = -radius; y <= radius; y++) {
        for(int x = -radius; x <= radius; x++) {
            // Increase the X-axis offset by stretchFactorX
            float weight = exp(-float((x * stretchFactorX) * (x * stretchFactorX) + y * y) / (radius * radius / 4.0));
            coord = fragmentTexCoord + vec2(texOffsetX * x * stretchFactorX, texOffsetY * y);
            bloom += texture(image, coord) * weight;
            totalWeight += weight;
        }
    }
    bloom /= totalWeight;

    // Adjust bloom intensity
    bloom *= bloomIntensity;

    // Get the original color of the image at this fragment
    vec4 originalColor = texture(image, fragmentTexCoord);

    // Modify screen blending to preserve more of the original image detail
    color = originalColor + (1.0 - originalColor) * bloom;
}
