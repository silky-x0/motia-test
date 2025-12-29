import { ApiRouteConfig } from 'motia'
import { z } from 'zod'

/**
 * API Step: Receives username generation requests
 * Emits 'username.requested' event for the Python step to process
 */

const bodySchema = z.object({
    theme: z.string().describe('The theme/style for usernames (e.g., gaming, aesthetic, professional)'),
    keywords: z.array(z.string()).optional().describe('Optional keywords to incorporate'),
    count: z.number().min(1).max(10).default(5).describe('Number of usernames to generate'),
})

export const config: ApiRouteConfig = {
    type: 'api',
    name: 'RequestUsernameGeneration',
    description: 'API endpoint to request AI-generated Instagram usernames',
    method: 'POST',
    path: '/api/generate-username',
    emits: ['username.requested'],
    bodySchema,
    flows: ['username-generator'],
}

export const handler = async (req: any, ctx: any) => {
    const { theme, keywords = [], count = 5 } = req.body

    ctx.logger.info('Username generation requested', { theme, keywords, count })

    // Emit event for Python step to process
    await ctx.emit({
        topic: 'username.requested',
        data: {
            theme,
            keywords,
            count,
            requestId: crypto.randomUUID(),
        },
    })

    return {
        status: 202,
        body: {
            message: 'Username generation started',
            theme,
            keywords,
            count,
        },
    }
}
