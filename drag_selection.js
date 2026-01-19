// Drag selection script for screenshot preview
(function() {
    function enableDragSelection() {
        // Find screenshot image (look for alt text or data attributes)
        let screenshots = Array.from(document.querySelectorAll('img')).filter(img => {
            return img.alt && img.alt.includes('Desktop Screenshot');
        });
        
        screenshots.forEach((img, idx) => {
            if (img.dataset.dragSelectionEnabled) return; // Skip if already processed
            img.dataset.dragSelectionEnabled = 'true';
            
            // Create container for canvas overlay
            const container = img.parentElement;
            container.style.position = 'relative';
            container.style.display = 'inline-block';
            
            // Create canvas for drawing selection
            const canvas = document.createElement('canvas');
            canvas.style.position = 'absolute';
            canvas.style.top = '0';
            canvas.style.left = '0';
            canvas.style.cursor = 'crosshair';
            canvas.style.zIndex = '100';
            canvas.style.display = 'block';
            canvas.style.pointerEvents = 'auto';
            
            // Size canvas to match image
            const updateCanvasSize = () => {
                if (img.naturalWidth > 0) {
                    canvas.width = img.naturalWidth;
                    canvas.height = img.naturalHeight;
                    canvas.style.width = img.offsetWidth + 'px';
                    canvas.style.height = img.offsetHeight + 'px';
                }
            };
            
            updateCanvasSize();
            if (!img.complete) {
                img.addEventListener('load', updateCanvasSize);
            }
            
            container.appendChild(canvas);
            
            let isDrawing = false;
            let startX, startY;
            
            const ctx = canvas.getContext('2d');
            
            const getCoordinates = (e) => {
                const rect = canvas.getBoundingClientRect();
                const scaleX = canvas.width / rect.width;
                const scaleY = canvas.height / rect.height;
                return {
                    x: (e.clientX - rect.left) * scaleX,
                    y: (e.clientY - rect.top) * scaleY
                };
            };
            
            const drawSelection = (fromX, fromY, toX, toY) => {
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                
                const x = Math.min(fromX, toX);
                const y = Math.min(fromY, toY);
                const w = Math.abs(toX - fromX);
                const h = Math.abs(toY - fromY);
                
                // Semi-transparent blue fill
                ctx.fillStyle = 'rgba(0, 100, 255, 0.2)';
                ctx.fillRect(x, y, w, h);
                
                // Blue border
                ctx.strokeStyle = '#0064FF';
                ctx.lineWidth = 2;
                ctx.strokeRect(x, y, w, h);
                
                // Corner handles
                const handleSize = 10;
                ctx.fillStyle = '#0064FF';
                const handles = [
                    {x: x, y: y}, {x: x + w, y: y},
                    {x: x, y: y + h}, {x: x + w, y: y + h}
                ];
                handles.forEach(h => {
                    ctx.fillRect(h.x - handleSize/2, h.y - handleSize/2, handleSize, handleSize);
                });
                
                // Display coordinates
                const text = `X: ${Math.round(x)}, Y: ${Math.round(y)}, W: ${Math.round(w)}, H: ${Math.round(h)}`;
                ctx.fillStyle = '#0064FF';
                ctx.font = 'bold 14px monospace';
                ctx.fillText(text, x + 15, y + 30);
            };
            
            // Draw initial preselected area from input fields
            const drawInitialSelection = () => {
                const inputs = document.querySelectorAll('input[type="number"]');
                let x = 0, y = 0, w = 640, h = 420;
                let foundCount = 0;
                
                inputs.forEach(input => {
                    const label = input.parentElement?.textContent || '';
                    if ((label.includes('X') || input.placeholder === 'X') && foundCount === 0) {
                        x = parseFloat(input.value) || 0;
                        foundCount++;
                    } else if ((label.includes('Y') || input.placeholder === 'Y') && foundCount === 1) {
                        y = parseFloat(input.value) || 0;
                        foundCount++;
                    } else if ((label.includes('Width') || input.placeholder === 'Width') && foundCount === 2) {
                        w = parseFloat(input.value) || 640;
                        foundCount++;
                    } else if ((label.includes('Height') || input.placeholder === 'Height') && foundCount === 3) {
                        h = parseFloat(input.value) || 420;
                        foundCount++;
                    }
                });
                
                if (w > 0 && h > 0) {
                    drawSelection(x, y, x + w, y + h);
                }
            };
            
            // Draw initial selection after a slight delay to ensure canvas is sized
            setTimeout(() => {
                if (canvas.width > 0 && canvas.height > 0) {
                    drawInitialSelection();
                }
            }, 100);
            
            canvas.addEventListener('mousedown', (e) => {
                isDrawing = true;
                const coords = getCoordinates(e);
                startX = coords.x;
                startY = coords.y;
            });
            
            canvas.addEventListener('mousemove', (e) => {
                if (!isDrawing) return;
                const coords = getCoordinates(e);
                drawSelection(startX, startY, coords.x, coords.y);
            });
            
            canvas.addEventListener('mouseup', (e) => {
                if (!isDrawing) return;
                isDrawing = false;
                
                const coords = getCoordinates(e);
                const x = Math.round(Math.min(startX, coords.x));
                const y = Math.round(Math.min(startY, coords.y));
                const w = Math.round(Math.abs(coords.x - startX));
                const h = Math.round(Math.abs(coords.y - startY));
                
                // Find and populate input fields
                const inputs = document.querySelectorAll('input[type="number"]');
                let xFound = false, yFound = false, wFound = false, hFound = false;
                
                inputs.forEach(input => {
                    const label = input.parentElement?.textContent || '';
                    if (!xFound && (label.includes('X') || input.placeholder === 'X')) {
                        input.value = x;
                        input.dispatchEvent(new Event('change', { bubbles: true }));
                        input.dispatchEvent(new Event('input', { bubbles: true }));
                        xFound = true;
                    } else if (!yFound && (label.includes('Y') || input.placeholder === 'Y')) {
                        input.value = y;
                        input.dispatchEvent(new Event('change', { bubbles: true }));
                        input.dispatchEvent(new Event('input', { bubbles: true }));
                        yFound = true;
                    } else if (!wFound && (label.includes('Width') || input.placeholder === 'Width')) {
                        input.value = w;
                        input.dispatchEvent(new Event('change', { bubbles: true }));
                        input.dispatchEvent(new Event('input', { bubbles: true }));
                        wFound = true;
                    } else if (!hFound && (label.includes('Height') || input.placeholder === 'Height')) {
                        input.value = h;
                        input.dispatchEvent(new Event('change', { bubbles: true }));
                        input.dispatchEvent(new Event('input', { bubbles: true }));
                        hFound = true;
                    }
                });
                
                // Keep selection visible - no timeout, always show
                drawSelection(x, y, x + w, y + h);
            });
            
            canvas.addEventListener('mouseleave', () => {
                if (isDrawing) {
                    isDrawing = false;
                }
            });
        });
    }
    
    // Run when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', enableDragSelection);
    } else {
        enableDragSelection();
    }
    
    // Watch for DOM changes (new images added)
    if (window.MutationObserver) {
        const observer = new MutationObserver(() => {
            setTimeout(enableDragSelection, 100);
        });
        observer.observe(document.body, {
            childList: true,
            subtree: true,
            attributes: false
        });
    }
})();
