#!/bin/bash
set -e

# Parse command line arguments
CHANGELOG_FILE=""
while [[ $# -gt 0 ]]; do
  case $1 in
    --changelog)
      CHANGELOG_FILE="$2"
      shift 2
      ;;
    *)
      echo "Unknown option $1"
      echo "Usage: $0 [--changelog <file>]"
      exit 1
      ;;
  esac
done

# Check if we have uncommitted changes
if ! git diff-index --quiet HEAD --; then
    echo "Error: You have uncommitted changes. Please commit or stash them first."
    exit 1
fi

# Get current version
CURRENT_VERSION=$(grep '^version = ' pyproject.toml | sed 's/version = "\(.*\)"/\1/')
echo "Current version: $CURRENT_VERSION"

# Increment patch version
IFS='.' read -ra VERSION_PARTS <<< "$CURRENT_VERSION"
MAJOR=${VERSION_PARTS[0]}
MINOR=${VERSION_PARTS[1]}
PATCH=${VERSION_PARTS[2]}
NEW_PATCH=$((PATCH + 1))
NEW_VERSION="$MAJOR.$MINOR.$NEW_PATCH"

echo "Bumping version to: $NEW_VERSION"

# Update version in pyproject.toml
sed -i "" "s/version = \"$CURRENT_VERSION\"/version = \"$NEW_VERSION\"/" pyproject.toml

# Commit version bump
git add pyproject.toml
git commit -m "bump version to $NEW_VERSION"

# Clean dist directory
rm -rf dist/*

# Build
echo "Building package..."
uv build

# Publish
echo "Publishing to PyPI..."
if [ -z "$PYPI_API_TOKEN" ]; then
    echo "Error: PYPI_API_TOKEN environment variable not set"
    exit 1
fi

uv publish --token "$PYPI_API_TOKEN"

# Build and push Docker image
echo "Building Docker image..."
docker build -t antidmg/toolfront:$NEW_VERSION .
docker build -t antidmg/toolfront:latest .

echo "Pushing Docker image..."
docker push antidmg/toolfront:$NEW_VERSION
docker push antidmg/toolfront:latest

# Push commit
git push

# Create and push tag
git tag "v$NEW_VERSION"
git push origin "v$NEW_VERSION"

# Create GitHub release
echo "Creating GitHub release..."
if [ -n "$CHANGELOG_FILE" ] && [ -f "$CHANGELOG_FILE" ]; then
    echo "Using changelog from: $CHANGELOG_FILE"
    gh release create "v$NEW_VERSION" --notes-file "$CHANGELOG_FILE" --title "v$NEW_VERSION"
else
    echo "Creating minimal release notes"
    gh release create "v$NEW_VERSION" --notes "Release v$NEW_VERSION" --title "v$NEW_VERSION"
fi

echo "Successfully released version $NEW_VERSION"
