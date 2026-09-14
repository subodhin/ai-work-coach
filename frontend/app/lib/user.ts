export function getUserId(): string {
  const key = "ai-work-coach-user-id";

  let userId = localStorage.getItem(key);

  if (!userId) {
    userId = crypto.randomUUID();
    localStorage.setItem(key, userId);
  }

  return userId;
}