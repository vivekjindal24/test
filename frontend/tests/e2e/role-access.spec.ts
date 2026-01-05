import { test, expect } from '@playwright/test'

const mockProjects = [{ id: 1, title: 'Thesis', description: 'Demo', status: 'draft' }]

test('redirects unauthenticated users to login', async ({ page }) => {
  await page.goto('/projects')
  await expect(page).toHaveURL(/.*\/login/)
})

test('allows authenticated role through guard and shows projects', async ({ page }) => {
  await page.route('**/projects', async (route) => {
    await route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(mockProjects) })
  })
  await page.goto('about:blank')
  await page.evaluate(() => {
    localStorage.setItem('access_token', 'fake')
    localStorage.setItem('role', 'student')
  })
  await page.goto('/projects')
  await expect(page.getByText('Projects')).toBeVisible()
  await expect(page.getByText('Thesis')).toBeVisible()
})
