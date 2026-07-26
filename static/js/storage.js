// js/storage.js
window.StorageService = {
    getObject(key, fallback) {
        try {
            const value = localStorage.getItem(key);
            return value ? JSON.parse(value) : fallback;
        } catch (error) {
            console.error(`Unable to load ${key}:`, error);
            return fallback;
        }
    },
 
    getArray(key) {
        const value = this.getObject(key, []);
        return Array.isArray(value) ? value : [];
    },
 
    saveObject(key, value) {
        localStorage.setItem(key, JSON.stringify(value));
    },
 
    getValue(key, fallback = null) {
        return localStorage.getItem(key) ?? fallback;
    },
 
    saveValue(key, value) {
        localStorage.setItem(key, value);
    }
};