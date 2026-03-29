---
title: "How to map an IDataRecord to an entity class object using expressions"
date: 2020-09-27
categories: ["Development", "Computers and Internet"]
tags: ["C#", "DbDataRecord", "DBNull", "IDataRecord", "Map"]
original_url: "https://williamforney.com/2020/09/27/how-to-map-an-idatarecord-to-an-entity-class-object-without-using-reflection/"
---

![blur close up code computer](/assets/img/posts/pexels-photo-546819.jpeg)

Recently I had a need to map an IDataRecord to an entity class object in C#. Here is the code for reference… First, we need the method that generates a function to map the properties while handling DBNull.
    
    
            private static Func<IDataReader, T> GenerateMapFunction<T>(IDataReader dataReader)
            {
                if (dataReader is null)
                {
                    throw new ArgumentNullException(nameof(dataReader));
                }
    
                var expressions = new List<Expression>();
    
                var dataReaderParameterExpression = Expression.Parameter(typeof(IDataRecord), "o7thDR");
    
                var targetExpression = Expression.Variable(typeof(T));
    
                expressions.Add(Expression.Assign(targetExpression, Expression.New(targetExpression.Type)));
    
                // does int based lookup
                var indexerInfo = typeof(IDataRecord).GetProperty("Item", new[] { typeof(int) });
    
                var columnNames = Enumerable.Range(0, dataReader.FieldCount)
                                            .Select(index => new { index, name = dataReader.GetName(index) });
    
                foreach (var column in columnNames)
                {
                    var property = targetExpression.Type.GetProperty(
                        column.name,
                        BindingFlags.Public | BindingFlags.Instance | BindingFlags.IgnoreCase);
                    if (property is null)
                    {
                        continue;
                    }
    
                    // index
                    var columnIndexExpression = Expression.Constant(column.index);
    
                    // reader
                    var readerPropertyExpression = Expression.MakeIndex(
                        dataReaderParameterExpression, indexerInfo, new[] { columnIndexExpression });
    
                    // reader.IsDBNull(index);
                    var isReaderDbNull = Expression.Call(
                        dataReaderParameterExpression, nameof(IDataReader.IsDBNull), null, columnIndexExpression);
    
                    // reader as PropertyType;
                    var safeCastExpression = Expression.TypeAs(
                        readerPropertyExpression,
                        property.PropertyType);
    
                    // T.Property
                    var targetPropertyExpression = Expression.Property(targetExpression, property);
    
                    // T.Property = reader.IsDBNull(index) ? default(PropertyType) :
                    // (PropertyType)reader as PropertyType;
                    var assignmentBlock = Expression.Condition(
                        Expression.IsTrue(isReaderDbNull),
                        Expression.Assign(
                            targetPropertyExpression,
                            Expression.Default(property.PropertyType)),
                        Expression.Assign(
                            targetPropertyExpression,
                            Expression.Convert(safeCastExpression, property.PropertyType)));
    
                    expressions.Add(assignmentBlock);
                }
    
                expressions.Add(targetExpression);
    
                return Expression.Lambda<Func<IDataReader, T>>(
                    Expression.Block(
                        new[] { targetExpression },
                        expressions),
                    dataReaderParameterExpression).Compile();
            }

Next we need the function that calls the above…
    
    
            public static T? Map<T>(this IDataReader dataReader) where T : class
            {
                if (dataReader is null)
                {
                    return default;
                }
    
                //// Use the following loop for debugging field data types in your entity classes.
                //for (var i = 0; i < dataReader.FieldCount; i++)
                //{
                //    Trace.TraceInformation($"{i}:{dataReader.GetName(i)} = {dataReader.GetFieldType(i).Name}");
                //}
    
                var converter = GenerateMapFunction<T>(dataReader);
                return converter(dataReader);
            }

This does the job for a single row, but we want all the rows in the reader, right? For that we need this one…
    
    
            public static List<T> ToList<T>(this IDataReader dataReader) where T : class  
            {  
                var list = new List<T>();  
      
                if (dataReader is not null)  
                {  
                    while (dataReader.Read())  
                    {  
                        var row = Map<T>(dataReader);  
                        if (row is not null)  
                        {  
                            list.Add(row);  
                        }  
                    }  
                }  
      
                return list;  
            }

That’s it… It doesn’t use the async API of the data reader for the read… We might want an async version too…
    
    
            public static async Task<List<T>> ToListAsync<T>(  
                this DbDataReader dataReader,  
                CancellationToken cancellationToken = default) where T : class  
            {  
                var list = new List<T>();  
      
                if (dataReader is not null)  
                {  
                    while (await dataReader.ReadAsync(cancellationToken).ConfigureAwait(false))  
                    {  
                        var row = Map<T>(dataReader);  
                        if (row is not null)  
                        {  
                            list.Add(row);  
                        }  
                    }  
                }  
      
                return list;  
            }  
    

But what if we don’t want to pull the whole list all at once? Then you need this…
    
    
            public static async IAsyncEnumerable<T> EnumerateAsync<T>(  
                this DbDataReader dataReader,  
                 CancellationToken cancellationToken = default) where T : class  
            {  
                if (dataReader is null)  
                {  
                    yield break;  
                }  
      
                while (await dataReader.ReadAsync(cancellationToken).ConfigureAwait(false))  
                {  
                    var row = Map<T>(dataReader);  
                    if (row is not null)  
                    {  
                        yield return row;  
                    }  
                }  
            }  
    

Oh, but what if you want a blocking version of that?
    
    
            public static IEnumerable<T> Enumerate<T>(this DbDataReader dataReader) where T : class  
            {  
                if (dataReader is null)  
                {  
                    yield break;  
                }  
      
                while (dataReader.Read())  
                {  
                    var row = Map<T>(dataReader);  
                    if (row is not null)  
                    {  
                        yield return row;  
                    }  
                }  
            }  
    

Hopefully, part of this will come in handy for someone as it was for me.

The code for this is available on (https://github.com/improvgroup/sharedcode) and via (https://www.nuget.org/packages/SharedCode.Data/).
