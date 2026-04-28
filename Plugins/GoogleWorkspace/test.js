const ctx = {
  api: {
    registerTool: (t) => {
      if (t.name === 'gog') {
        t.execute({ args: 'tasks add --add "task 1" --add "task 2"' })
          .then(console.log)
          .catch(console.error);
      }
    },
    on: () => {}
  }
};
require('./dist/index.js').default(ctx);
