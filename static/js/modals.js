// js/modals.js
window.ModalService = {
    activeModalId: null,
    previouslyFocusedElement: null,
 
    open(id) {
        const modal = document.getElementById(id);
        if (!modal) return;
 
        this.previouslyFocusedElement = document.activeElement;
        this.activeModalId = id;
 
        modal.classList.add("visible");
        modal.setAttribute("aria-hidden", "false");
 
        const focusTarget = modal.querySelector(
            "button, input, textarea, select"
        );
 
        focusTarget?.focus();
    },
 
    close(id) {
        const modal = document.getElementById(id);
        if (!modal) return;
 
        modal.classList.remove("visible");
        modal.setAttribute("aria-hidden", "false");
 
        if (this.activeModalId === id) {
            this.activeModalId = null;
            this.previouslyFocusedElement?.focus();
        }
    },
 
    closeActive() {
        if (this.activeModalId) {
            this.close(this.activeModalId);
        }
    },
 
    bindCloseButton(buttonId, modalId) {
        document.getElementById(buttonId)?.addEventListener("click", () => {
            this.close(modalId);
        });
    },
 
    bindBackdropClose(modalId) {
        document.getElementById(modalId)?.addEventListener("click", event => {
            if (event.target.id === modalId) {
                this.close(modalId);
            }
        });
    }
};