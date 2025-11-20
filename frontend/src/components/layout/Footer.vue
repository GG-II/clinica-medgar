<template>
  <footer class="footer">
    <div class="footer-content">
      <div class="footer-left">
        <p class="text-sm text-gray-600">
          © 2025 <strong>Clínica Médica Dra. Estephanny García</strong>
        </p>
        <p class="text-xs text-gray-500 mt-1">
          Sistema de Gestión Clínica v1.0.0
        </p>
      </div>

      <div class="footer-right">
        <a href="#" class="footer-link">Soporte</a>
        <span class="text-gray-300">|</span>
        <a href="#" class="footer-link">Documentación</a>
        <span class="text-gray-300">|</span>
        <a href="#" class="footer-link">Términos de Uso</a>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  background: white;
  border-top: 1px solid #e5e7eb;
  padding: 1rem 1.5rem;
  margin-top: auto;
}

.footer-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 100%;
}

.footer-left {
  flex: 1;
}

.footer-right {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.footer-link {
  font-size: 0.875rem;
  color: #6b7280;
  transition: color 0.2s;
}

.footer-link:hover {
  color: #8b5cf6;
}

@media (max-width: 640px) {
  .footer-content {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }

  .footer-right {
    flex-wrap: wrap;
    justify-content: center;
  }
}
</style>