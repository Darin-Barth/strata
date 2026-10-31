// One-time skill refund for the skill tree redesign (docs/skill-trees-rework.md, after 1.1.0): the Combat,
// Mining and Fishing trees changed layout and XP curve, so the first time each player logs in afterwards their
// unlocked nodes in those trees are reset and every point comes back to spend. XP is kept (it now buys fewer
// levels on the slower curve). The magic trees didn't change and keep their nodes.
// Bump strataSkillsRefundVersion if a later redesign needs another refund.
// KubeJS server scripts share one scope: every top-level name here starts with "strataSkillsRefund".
const strataSkillsRefundVersion = 2
const strataSkillsRefundCategories = ['puffish_skills:combat', 'puffish_skills:mining', 'strata:fishing']

PlayerEvents.loggedIn(event => {
  const player = event.player
  const data = player.persistentData
  if (data.getInt('strata_skills_refund') >= strataSkillsRefundVersion) return
  const name = player.getGameProfile().getName()
  strataSkillsRefundCategories.forEach(c => event.server.runCommandSilent(`puffish_skills skills reset ${name} ${c}`))
  data.putInt('strata_skills_refund', strataSkillsRefundVersion)
  player.tell(Text.gold('The Combat, Mining and Fishing skill trees were redesigned: bigger trees, more keystones, '
    + 'and a slower climb. Your points have been refunded, so open your skills (Ctrl+K) and spend them again.'))
})
