---
title: "Using a wait cursor doesn’t have to be hard…"
date: 2020-09-27
categories: ["Development", "Computers and Internet"]
tags: ["cursor", "wait", "wait cursor", "WaitCursor", "Windows Forms"]
original_url: "https://williamforney.com/2020/09/27/using-a-wait-cursor-doesnt-have-to-be-hard/"
---

![animal cute little mouse](/assets/img/posts/pexels-photo-301448.jpeg)

Here is a simple disposable wait cursor class to simplify your mouse display needs…
    
    
        /// <summary>
        /// The WaitCursor class. Implements the <see cref="IDisposable" />
        /// </summary>
        /// <seealso cref="IDisposable" />
        public class WaitCursor : IDisposable
        {
            /// <summary>
            /// The previous cursor.
            /// </summary>
            private readonly Cursor previousCursor;
    
            /// <summary>
            /// A value indicating whether the class has been disposed.
            /// </summary>
            private bool disposedValue;
    
            /// <summary>
            /// Initializes a new instance of the <see cref="WaitCursor" /> class.
            /// </summary>
            public WaitCursor()
            {
                this.previousCursor = Cursor.Current;
                Cursor.Current = Cursors.WaitCursor;
            }
    
            /// <summary>
            /// Finalizes an instance of the <see cref="WaitCursor" /> class.
            /// </summary>
            ~WaitCursor()
            {
                this.Dispose(disposing: false);
            }
    
            /// <summary>
            /// Performs application-defined tasks associated with freeing, releasing, or resetting
            /// unmanaged resources.
            /// </summary>
            public void Dispose()
            {
                this.Dispose(disposing: true);
                GC.SuppressFinalize(this);
            }
    
            /// <summary>
            /// Releases unmanaged and - optionally - managed resources.
            /// </summary>
            /// <param name="disposing">
            /// <c>true</c> to release both managed and unmanaged resources; <c>false</c> to release
            /// only unmanaged resources.
            /// </param>
            protected virtual void Dispose(bool disposing)
            {
                if (!this.disposedValue)
                {
                    if (disposing)
                    {
                    }
    
                    Cursor.Current = this.previousCursor;
    
                    this.disposedValue = true;
                }
            }
        }
