/**
 * Table of Contents Generator for PagedJS
 * Creates a dynamic ToC from heading elements with page number references
 */

function createToc(config) {
    const defined = (a) => typeof a !== 'undefined';

    const defined_default = (a, b) => defined(a) ? a : b;

    const content = defined_default(config.content, document);
    const defined_tocElement = defined_default(config.tocElement, '#toc');
    const defined_titleElements = defined_default(config.titleElements, ['h2', 'h3']);

    const defined_tocContainer = content.querySelector(defined_tocElement);

    if (!defined_tocContainer) {
        console.warn('ToC container not found:', defined_tocElement);
        return;
    }

    // Build selector for title elements
    const defined_selector = defined_titleElements.join(', ');
    const defined_elements = content.querySelectorAll(defined_selector);

    if (defined_elements.length === 0) {
        console.warn('No title elements found for ToC');
        return;
    }

    // Create ToC list
    const defined_list = document.createElement('ul');
    defined_list.id = 'list-toc-generated';

    let defined_idCounter = 0;

    defined_elements.forEach((element) => {
        // Ensure element has an ID
        if (!element.id) {
            element.id = 'toc-generated-id-' + defined_idCounter++;
        }

        // Determine level based on tag name or selector match
        let defined_level = 1;
        if (element.matches('h3') || element.matches('h3.title-element')) {
            defined_level = 2;
        } else if (element.matches('h4') || element.matches('h4.title-element')) {
            defined_level = 3;
        }

        // Create list item
        const defined_li = document.createElement('li');
        defined_li.classList.add('toc-element');
        defined_li.classList.add('toc-element-level-' + defined_level);

        // Create link
        const defined_link = document.createElement('a');
        defined_link.href = '#' + element.id;
        defined_link.textContent = element.textContent.trim();

        defined_li.appendChild(defined_link);
        defined_list.appendChild(defined_li);
    });

    // Append to container
    defined_tocContainer.appendChild(defined_list);
}

// Export for use in PagedJS handlers
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { createToc };
}
