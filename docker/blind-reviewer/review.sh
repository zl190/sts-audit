#!/usr/bin/env bash
# Blind paper review via Docker-isolated container.
#
# Usage:
#   ./docker/blind-reviewer/review.sh paper/STS_Finance_Paper_v13.md
#   ./docker/blind-reviewer/review.sh paper/paper.md path/to/custom_spec.md
#   REVIEWER_MODEL=claude-opus-4-6 ./docker/blind-reviewer/review.sh paper/paper.md
#
# Environment:
#   ANTHROPIC_API_KEY  — required
#   REVIEWER_MODEL     — optional (default: claude-sonnet-4-5-20250929)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# --- Arguments ---
PAPER="${1:?Usage: $0 <paper.md> [spec.md] [output_dir]}"
SPEC="${2:-$SCRIPT_DIR/specs/reviewer.md}"
OUTPUT_DIR="${3:-$PROJECT_ROOT/output/reviews}"

# --- Validate ---
if [[ -z "${ANTHROPIC_API_KEY:-}" ]]; then
    echo "ERROR: ANTHROPIC_API_KEY not set." >&2
    exit 1
fi

if [[ ! -f "$PAPER" ]]; then
    echo "ERROR: Paper not found: $PAPER" >&2
    exit 1
fi

if [[ ! -f "$SPEC" ]]; then
    echo "ERROR: Spec not found: $SPEC" >&2
    exit 1
fi

# --- Resolve absolute paths ---
PAPER="$(cd "$(dirname "$PAPER")" && pwd)/$(basename "$PAPER")"
SPEC="$(cd "$(dirname "$SPEC")" && pwd)/$(basename "$SPEC")"
mkdir -p "$OUTPUT_DIR"
OUTPUT_DIR="$(cd "$OUTPUT_DIR" && pwd)"

# --- Build image (if needed) ---
IMAGE_NAME="sts-blind-reviewer"
echo "Building Docker image..."
docker build -q -t "$IMAGE_NAME" "$SCRIPT_DIR"

# --- Run ---
echo ""
echo "=== Blind Review ==="
echo "Paper:  $PAPER"
echo "Spec:   $SPEC"
echo "Output: $OUTPUT_DIR/"
echo "Model:  ${REVIEWER_MODEL:-claude-sonnet-4-5-20250929}"
echo ""

docker run --rm \
    -e ANTHROPIC_API_KEY="$ANTHROPIC_API_KEY" \
    ${REVIEWER_MODEL:+-e REVIEWER_MODEL="$REVIEWER_MODEL"} \
    -v "$SPEC":/input/spec.md:ro \
    -v "$PAPER":/input/paper.md:ro \
    -v "$OUTPUT_DIR":/output/ \
    "$IMAGE_NAME"

echo ""
echo "=== Review Complete ==="
echo "Output: $(ls -t "$OUTPUT_DIR"/review_*.md 2>/dev/null | head -1)"
