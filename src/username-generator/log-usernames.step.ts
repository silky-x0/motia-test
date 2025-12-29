import { EventConfig } from 'motia'
import { z } from 'zod'

/**
 * Event Step: Logs the generated usernames
 * Subscribes to 'username.generated' to display results
 */

const inputSchema = z.object({
    requestId: z.string(),
    success: z.boolean(),
    theme: z.string().optional(),
    keywords: z.array(z.string()).optional(),
    usernames: z.array(z.string()),
    error: z.string().optional(),
})

export const config: EventConfig = {
    type: 'event',
    name: 'LogGeneratedUsernames',
    description: 'Logs and processes the AI-generated usernames',
    subscribes: ['username.generated'],
    emits: [],
    input: inputSchema,
    flows: ['username-generator'],
}

export const handler = async (input: any, ctx: any) => {
    const { requestId, success, theme, usernames, error } = input

    if (success) {
        ctx.logger.info('✅ Usernames generated successfully!', {
            requestId,
            theme,
            count: usernames.length,
        })

        // Log each username
        usernames.forEach((username: string, index: number) => {
            ctx.logger.info(`  ${index + 1}. @${username}`)
        })

        // Store results in state for retrieval
        await ctx.state.set('usernames', requestId, {
            theme,
            usernames,
            generatedAt: new Date().toISOString(),
        })
    } else {
        ctx.logger.error('❌ Username generation failed', { requestId, error })
    }
}
