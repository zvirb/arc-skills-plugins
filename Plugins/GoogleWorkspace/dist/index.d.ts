export interface PluginApi {
    registerTool(tool: any): void;
    on(event: string, callback: () => void): void;
}
export declare const manifest: {
    name: string;
    version: string;
    configSchema: {
        type: string;
        properties: {
            composioApiKey: {
                type: string;
            };
        };
    };
};
export default function register(ctx: any, second: any): void;
