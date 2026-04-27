import { PluginApi } from '@openclaw/plugin-sdk';
export declare const manifest: {
    name: string;
    version: string;
    configSchema: {
        type: string;
        properties: {
            composioApiKey: {
                type: string;
            };
            subAgentModel: {
                type: string;
                default: string;
            };
        };
        required: string[];
    };
};
export default function register(api: PluginApi, config: any): void;
