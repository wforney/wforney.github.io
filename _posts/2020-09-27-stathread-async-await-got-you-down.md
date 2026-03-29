---
title: "STAThread async/await got you down?"
date: 2020-09-27
categories: ["Development", "Computers and Internet"]
tags: ["async", "await", "C#", "STA", "SynchronizationContext", "Windows Forms"]
original_url: "https://williamforney.com/2020/09/27/stathread-async-await-got-you-down/"
---

![abstract business code coder](https://williamforney.com/wp-content/uploads/2020/09/pexels-photo-270348.jpeg)

When encountering issues with async/await while building a Windows Forms application recently I came across this helpful class that allows you to await returning to the initial (usually UI) thread…
    
    
    public struct SynchronizationContextAwaiter : INotifyCompletion, IEquatable<SynchronizationContextAwaiter>
        {
            private static readonly SendOrPostCallback postCallback = state => (state as Action)?.Invoke();
    
            private readonly SynchronizationContext context;
    
            public SynchronizationContextAwaiter(SynchronizationContext context) => this.context = context;
    
            public bool IsCompleted => context == SynchronizationContext.Current;
    
            public static bool operator !=(SynchronizationContextAwaiter left, SynchronizationContextAwaiter right) =>
                !(left == right);
    
            public static bool operator ==(SynchronizationContextAwaiter left, SynchronizationContextAwaiter right) =>
                left.Equals(right);
    
            public override bool Equals(object? obj) =>
                obj is SynchronizationContextAwaiter awaiter && this.Equals(awaiter);
    
            public bool Equals(SynchronizationContextAwaiter other) =>
                EqualityComparer<SynchronizationContext>.Default.Equals(this.context, other.context);
    
            public override int GetHashCode() => HashCode.Combine(this.context);
    
            [SuppressMessage("Performance", "CA1822:Mark members as static", Justification = "Reviewed.")]
            public void GetResult()
            {
            }
    
            public void OnCompleted(Action continuation) => context.Post(postCallback, continuation);
        }

It goes along with this extension method…
    
    
            /// <summary>
            /// Gets an awaiter for the specified synchronization context.
            /// </summary>
            /// <param name="context">The synchronization context.</param>
            /// <returns>The <see cref="SynchronizationContextAwaiter"/>.</returns>
            public static SynchronizationContextAwaiter GetAwaiter(this SynchronizationContext context) =>
                new SynchronizationContextAwaiter(context);

And you use it like this…
    
    
                    var syncContext = SynchronizationContext.Current; // Grab UI thread
    
                    // TODO: Do long running async stuff here
    
                    if (syncContext != null)
                    {
                        await syncContext;
                    }
    
                    // TODO: Do original/UI thread stuff here

This is a somewhat cleaner way to handle the multi-threading problem in async methods in a STAThread application.
