// Function to scroll highlighted lines into view
function scrollHighlightedLines() {
  // Find all code blocks
  const codeBlocks = document.querySelectorAll('.code-block-root');
  
  codeBlocks.forEach(block => {
    // Find the scrollable viewport within this code block
    const viewport = block.querySelector('[data-radix-scroll-area-viewport]');
    
    if (viewport) {
      // Find all highlighted lines within this code block
      const highlightedLines = block.querySelectorAll('.code-block-line.highlight');
      
      if (highlightedLines.length > 0) {
        // If there are multiple highlighted lines, scroll to the first one
        const firstHighlightedLine = highlightedLines[0];
        
        // Scroll the line into view
        firstHighlightedLine.scrollIntoView({
          behavior: 'auto',
          block: 'center' // Centers the line in the visible area
        });
      }
    }
  });
}

// Run when the page loads
document.addEventListener('DOMContentLoaded', scrollHighlightedLines);

// Also run when the page is fully loaded (in case DOMContentLoaded fired too early)
if (document.readyState === 'complete') {
  scrollHighlightedLines();
} 