#!/bin/bash

# Initialize git repository
git init

# Add all files
git add .

# Make initial commit
git commit -m "Initial commit: ImageFX Generator with lightbox preview and improved UI"

echo "Repository initialized and first commit created!"
echo "Next steps:"
echo "1. Create a new repository on GitHub"
echo "2. Add the remote repository:"
echo "   git remote add origin https://github.com/yourusername/imagefx-generator.git"
echo "3. Push your code:"
echo "   git push -u origin main" 