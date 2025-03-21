// Function to scroll highlighted lines into view
function scrollHighlightedLines() {
  document.querySelectorAll('.code-block-root').forEach(block => {
    const viewport = block.querySelector('[data-radix-scroll-area-viewport]');
    if (viewport) {
      const highlightedLines = block.querySelectorAll('.code-block-line.highlight');
      if (highlightedLines.length > 0) {
        const firstHighlightedLine = highlightedLines[0];
        const allLines = block.querySelectorAll('.code-block-line');
        const lineHeight = firstHighlightedLine.clientHeight;
        const viewportHeight = viewport.clientHeight;
        const visibleLines = Math.floor(viewportHeight / lineHeight);
        // -1 because it looks better in my opinion
        const linesAbove = Math.floor(visibleLines / 2) - 1;
        
        viewport.scrollTop = firstHighlightedLine.offsetTop - (linesAbove * lineHeight);
      }
    }
  });
}

// Run on initial load and navigation
scrollHighlightedLines();
document.addEventListener('DOMContentLoaded', scrollHighlightedLines);

if (typeof window !== 'undefined') {
  window.addEventListener('popstate', scrollHighlightedLines);
  document.addEventListener('next-navigation', scrollHighlightedLines);
  document.addEventListener('routeChangeComplete', scrollHighlightedLines);
  
  const observer = new MutationObserver(scrollHighlightedLines);
  observer.observe(document.body, { childList: true, subtree: true });
} 