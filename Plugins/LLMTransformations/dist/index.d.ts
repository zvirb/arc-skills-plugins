import { PluginApi } from '@openclaw/plugin-sdk';
export declare const manifest: {
    name: string;
    version: string;
    configSchema: {
        type: string;
        properties: {
            defaultModel: {
                type: string;
                default: string;
            };
        };
    };
};
export default function register(api: PluginApi, config: any): void;
