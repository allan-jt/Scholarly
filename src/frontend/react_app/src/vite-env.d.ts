/// <reference types="vite/client" />

interface ImportMeta {
	readonly env: ImportMetaEnv
}

interface ImportMetaEnv {
	readonly VITE_BACKEND_URL: string
	readonly VITE_HOST: string
	readonly VITE_PORT: string
}
