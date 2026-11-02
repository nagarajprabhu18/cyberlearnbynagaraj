import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { cleanup, render, screen, waitFor } from '@testing-library/react';
import App from './App';

describe('CyberLearn landing page', () => {
  beforeEach(() => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ ok: true, json: async () => [] }));
  });

  afterEach(() => {
    cleanup();
    vi.unstubAllGlobals();
  });

  it('shows the learning paths and loads the published course catalog', async () => {
    render(<App />);
    expect(screen.getByRole('heading', { name: /build skills/i })).toBeInTheDocument();
    expect(screen.getByRole('link', { name: /networking & ccna/i })).toBeInTheDocument();
    await waitFor(() => expect(fetch).toHaveBeenCalledWith('http://localhost:8000/api/v1/courses', expect.any(Object)));
    expect(await screen.findByText('No published courses yet')).toBeInTheDocument();
  });
});
